#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Document Parsing Dependencies Installer
# For: analyse-fsd skill (Kilo)
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/install.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "${msg}" >> "${LOG_FILE}"
    echo -e "${msg}"
}

error() {
    log "${RED}ERROR: $1${NC}"
    exit 1
}

success() {
    log "${GREEN}✓ $1${NC}"
}

warn() {
    log "${YELLOW}⚠ $1${NC}"
}

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON=python3
    elif command -v python &> /dev/null; then
        PYTHON=python
    else
        error "Python not found. Please install Python 3.8+ first."
    fi

    PY_VERSION=$(${PYTHON} -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo "${PY_VERSION}" | cut -d. -f1)
    PY_MINOR=$(echo "${PY_VERSION}" | cut -d. -f2)

    if [[ "${PY_MAJOR}" -lt 3 ]] || [[ "${PY_MAJOR}" -eq 3 && "${PY_MINOR}" -lt 8 ]]; then
        error "Python 3.8+ required. Found: ${PY_VERSION}"
    fi
    success "Python ${PY_VERSION} detected"
}

# Check pip
check_pip() {
    if ${PYTHON} -m pip --version &> /dev/null; then
        PIP="${PYTHON} -m pip"
        success "pip available"
    elif command -v pip3 &> /dev/null; then
        PIP="pip3"
        success "pip3 available"
    elif command -v pip &> /dev/null; then
        PIP="pip"
        success "pip available"
    else
        error "pip not found. Please install pip first."
    fi
}

# Install a package with retry
install_package() {
    local pkg="$1"
    local import_name="${2:-$1}"

    # Check if already installed
    if ${PYTHON} -c "import ${import_name}" 2>/dev/null; then
        success "${pkg} already installed"
        return 0
    fi

    log "Installing ${pkg}..."
    if ${PIP} install "${pkg}" --quiet --disable-pip-version-check 2>>"${LOG_FILE}"; then
        # Verify installation
        if ${PYTHON} -c "import ${import_name}" 2>/dev/null; then
            success "${pkg} installed successfully"
            return 0
        fi
    fi

    warn "Failed to install ${pkg}, trying with --user flag..."
    if ${PIP} install "${pkg}" --user --quiet --disable-pip-version-check 2>>"${LOG_FILE}"; then
        success "${pkg} installed (user mode)"
        return 0
    fi

    error "Failed to install ${pkg}. Check ${LOG_FILE} for details."
}

# Main installation
main() {
    log "═══════════════════════════════════════════"
    log "Document Parsing Dependencies Installer"
    log "═══════════════════════════════════════════"

    check_python
    check_pip

    log ""
    log "Installing core dependencies..."

    # Document parsing
    install_package "python-docx" "docx"
    install_package "pdfplumber" "pdfplumber"
    install_package "openpyxl" "openpyxl"

    # Data processing
    install_package "pandas" "pandas"
    install_package "tabulate" "tabulate"

    # CSV encoding detection
    install_package "chardet" "chardet"

    log ""
    log "═══════════════════════════════════════════"
    success "All dependencies installed successfully!"
    log "═══════════════════════════════════════════"
    log ""
    log "You can now parse documents:"
    log "  python scripts/parse_docx.py <file.docx>"
    log "  python scripts/parse_pdf.py <file.pdf>"
    log "  python scripts/parse_xlsx.py <file.xlsx>"
    log "  python scripts/parse_csv.py <file.csv>"
    log "  python scripts/parse_md.py <file.md>"
}

main "$@"
