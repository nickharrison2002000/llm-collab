# Real HackerOne Report Example (Arc Remote Signer Unauthenticated Signing)

Use this as the gold-standard structure and tone for high-quality, high-impact reports.

## Summary

The Arc Remote Signer exposes its signing service (`arc.signer.v1.SignerService`) over **unauthenticated gRPC**, bound to `0.0.0.0` with TLS disabled by default. There is no authentication, authorization, or client-identity verification in the request path. Any host with network reachability can submit an arbitrary message and receive a valid signature under the validator's private key without presenting credentials.

This is a **full key-abuse primitive**: while the attacker never obtains the key material (it remains in the Nitro Enclave), they can exercise the signing key as if they held it.

## Verified Code Path

Every component was verified against current `main` branch:

1. **`internal/app/public/public.go`** — Builds the public server with `pb.RegisterSignerServiceServer(grpcSrv, params.SignerSvc)` and enables `reflection.Register(grpcSrv)`, publishing the full service schema to unauthenticated clients

2. **`internal/common/grpc/server/server.go` (NewServer)** — The complete unary interceptor chain is: `WithRecovery`, `WithRequestID`, `WithMetrics`, `WithLogging`, plus optional Prometheus metrics. **No authentication or authorization interceptor exists** anywhere in the codebase

3. **`internal/app/service/signer/signer.go:208` (Service.Sign)** — Validates only that the request is non-nil and message is non-empty, then forwards to the enclave for signing. **No caller identity is checked or inspected**

4. **`internal/app/config.go:87-92` and `configs/app.yaml`** — Default configuration: `host: 0.0.0.0`, `port: 10340` (dev) / `8080` (default), `tls.enabled: false`

5. **`proto/arc/signer/v1/signer.proto`** — Wire contract: `Sign(SignRequest{bytes message})` returns `(SignResponse{bytes signature})`. **No auth token, session, or identity field exists in the protocol**

## Steps To Reproduce

The repository ships a complete local development stack (LocalStack for KMS/Secrets Manager mocks, containerized local enclave), so this can be demonstrated **without AWS credentials**.

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/circlefin/arc-remote-signer && cd arc-remote-signer
   ```

2. Start dependencies (LocalStack + local enclave):
   ```bash
   make up
   ```

3. In a second terminal, start the application (listens on `0.0.0.0:10340`, TLS disabled):
   ```bash
   make dev
   ```

### Execute Proof of Concept

4. Run the attached PoC (`poc_unauth_sign.go`):
   ```bash
   go run poc_unauth_sign.go --addr 127.0.0.1:10340
   ```

The PoC performs:
- gRPC reflection list (confirms service is enumerable without credentials)
- `PublicKey` RPC (returns validator public key)
- `Sign` RPC over attacker-chosen message
- Ed25519 cryptographic verification of the returned signature

## Verified Evidence

**Test Environment:** Repository `main` branch (commit `a9e9fdb48c1e96a6c3fb875aba3d341e6a8af1a6`), full local stack via `make up`, app via `make dev`, Ubuntu 26.04, Go 1.25. No AWS credentials used.

**Server startup log** (showing genuine enclave-held key):
```
{"level":"INFO","msg":"loaded signer public key","logger":"service.signer",
 "public_key":"0xd51aab57d3d2163d771f73c5e2124fdb1f33b17d75bed1d22d7cc8c93f5788f3"}
gRPC server listening on [::]:10340
```

**PoC client output** (no credentials, no TLS, no authentication metadata):
```
root@uncleNickypoo:~/arc-remote-signer# go run poc_unauth_sign.go --addr 127.0.0.1:10340
----- BEGIN RAW RESPONSE -----
addr:      127.0.0.1:10340
payload:   POC: attacker-controlled message signed by validator key
pubkey:    d51aab57d3d2163d771f73c5e2124fdb1f33b17d75bed1d22d7cc8c93f5788f3
signature: ca3baf5b03d1eb683aae29cccaf4338220b46f76b7139cb541fe3787d60013b587e6edcb2edcbdb69f1d3d003a096d257affd9b6067908ac13871a3862a37403
verified:  true
----- END RAW RESPONSE -----
```

**Key Evidence:**
- Public key returned by unauthenticated `PublicKey` RPC is **byte-identical** to the key logged at server startup
- Ed25519 verification returned `true`: valid signature over attacker-chosen message
- Client used insecure transport with zero credentials
- Server bound to `[::]:10340` (all interfaces)

## Supporting Material/References

* `poc_unauth_sign.go` — Complete proof-of-concept demonstrating unauthenticated signing

## Impact

An attacker with network access to the Arc Remote Signer can **forge arbitrary signatures** under the validator's private key without any authentication. This completely undermines the security model of the validator infrastructure.

### Direct Consequences

1. **Validator Impersonation** — Attacker can sign any blockchain message (blocks, attestations, votes) as if they were the legitimate validator, without ever compromising the private key material

2. **Slashing Risk** — Attacker can create conflicting signatures (double-signing, surround votes) that trigger slashing conditions, resulting in loss of staked funds for the validator operator

3. **Network Disruption** — Malicious signatures can be injected into the blockchain network to disrupt consensus or create forks

4. **Reputation/Trust Damage** — Validator appears to be misbehaving from the network's perspective, damaging trust even if the key material was never compromised

### Exploitation Scenario

```
1. Attacker discovers Arc Remote Signer exposed on public IP (e.g., through Shodan, network scanning)
2. Attacker connects to port 10340/8080 via plaintext gRPC (no TLS required)
3. Attacker retrieves validator public key via unauthenticated PublicKey RPC
4. Attacker crafts malicious blockchain messages (e.g., conflicting attestations)
5. Attacker submits messages to Sign RPC and receives valid signatures
6. Attacker broadcasts signed messages to blockchain network
7. Validator is slashed or banned for apparent misbehavior
```

### Attack Prerequisites

- Network reachability to the gRPC port (default: `0.0.0.0:10340` or `0.0.0.0:8080`)
- No authentication credentials required
- Works over plaintext connection (TLS disabled by default)

This vulnerability provides a **complete abuse primitive** equivalent to key compromise, except the attacker doesn't need to extract the key—they can simply use the signing service directly.
