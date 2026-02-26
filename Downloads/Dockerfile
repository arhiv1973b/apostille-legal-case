FROM alpine:latest

WORKDIR /evidence

# Copy apostilles
COPY Apostilles ./Apostilles/

# Copy documentation files
COPY APOSTILLE_INVESTIGATION_SUMMARY.md ./
COPY LEGAL_TIMELINE.md ./
COPY EVIDENCE_CHAIN.md ./
COPY LEGAL_ANALYSIS.md ./
COPY README.md ./

# Install basic utilities
RUN apk add --no-cache bash curl git

# Create manifest
RUN echo "MACERET CASE EVIDENCE CONTAINER" > /evidence/MANIFEST.txt &&     echo "Apostilles: 0" >> /evidence/MANIFEST.txt &&     echo "Documentation: 0" >> /evidence/MANIFEST.txt

CMD ["bash"]
