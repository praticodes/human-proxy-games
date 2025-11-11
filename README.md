# Hanabi-Human-Proxies
This repository is for playing games with the Hanabi Human Proxies provided in the official repository created by
the authors of the [AH2AC2 Paper](https://ah2ac2.com/): https://github.com/FLAIROx/ah2ac2/tree/production.

## Common Errors and Debug Information

### SSL Certificate Verification Issue
If you see an error similar to `ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local 
      issuer certificate`, try the following steps:

1. `pip install certifi`
2. `export REQUESTS_CA_BUNDLE=/path/to/certifi/cacert.pem` (for example, `export SSL_CERT_FILE=/opt/anaconda3/lib/python3.13/site-packages/certifi/cacert.pem`)

This will ensure Python has the necessary certificates to securely connect to the server.

## Attributions
- All code for running and training human proxy agents is provided by the authors of the [AH2AC2 Paper](https://ah2ac2.com/),
whose repository we have forked.