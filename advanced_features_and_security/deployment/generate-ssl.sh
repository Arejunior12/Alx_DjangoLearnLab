#!/bin/bash
# Script to generate self-signed SSL certificate for testing
# For production, use certificates from Let's Encrypt or a trusted CA

DOMAIN="localhost"

echo "Generating SSL certificate for $DOMAIN..."

# Create directory for certificates
mkdir -p ssl_certs
cd ssl_certs

# Generate private key
openssl genrsa -out $DOMAIN.key 2048

# Generate CSR
openssl req -new -key $DOMAIN.key -out $DOMAIN.csr -subj "/CN=$DOMAIN"

# Generate self-signed certificate
openssl x509 -req -days 365 -in $DOMAIN.csr -signkey $DOMAIN.key -out $DOMAIN.crt

echo "SSL certificate generated:"
echo "Key: ssl_certs/$DOMAIN.key"
echo "Certificate: ssl_certs/$DOMAIN.crt"
echo ""
echo "For production, replace these with certificates from a trusted Certificate Authority."