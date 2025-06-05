#!/bin/bash
# MIRRALISM V2 Migration Installer - Quick Setup Script
# =====================================================

set -e  # Exit on any error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_DIR="$PROJECT_ROOT/scripts"

echo "🚀 MIRRALISM V2 Quick Installation"
echo "=================================="
echo "Project Root: $PROJECT_ROOT"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}$message${NC}"
}

# Check if running from correct directory
if [ ! -f "$PROJECT_ROOT/CLAUDE.md" ]; then
    print_status $RED "❌ CLAUDE.md not found. Please run from MIRRALISM_V2 root directory."
    exit 1
fi

# Step 1: Check dependencies
print_status $BLUE "🔍 Step 1: Checking dependencies..."
if command -v python3 >/dev/null 2>&1; then
    print_status $GREEN "✅ Python3 found: $(python3 --version)"
else
    print_status $RED "❌ Python3 not found. Please install Python 3.9 or later."
    exit 1
fi

if command -v node >/dev/null 2>&1; then
    print_status $GREEN "✅ Node.js found: $(node --version)"
else
    print_status $RED "❌ Node.js not found. Please install Node.js 18 or later."
    exit 1
fi

if command -v git >/dev/null 2>&1; then
    print_status $GREEN "✅ Git found: $(git --version)"
else
    print_status $RED "❌ Git not found. Please install Git."
    exit 1
fi

# Step 2: Get current date using MIRRALISM date system
print_status $BLUE "📅 Step 2: Verifying MIRRALISM date system..."
if [ -f "$SCRIPT_DIR/getDate.js" ]; then
    node "$SCRIPT_DIR/getDate.js"
    print_status $GREEN "✅ Date system verified"
else
    print_status $RED "❌ getDate.js not found"
    exit 1
fi

# Step 3: Run dependency check
print_status $BLUE "🔧 Step 3: Running dependency check..."
if python3 "$SCRIPT_DIR/migrate_installer.py" check; then
    print_status $GREEN "✅ Dependencies verified"
else
    print_status $RED "❌ Dependency check failed"
    exit 1
fi

# Step 4: Create initial backup
print_status $BLUE "💾 Step 4: Creating backup..."
backup_output=$(python3 "$SCRIPT_DIR/migrate_installer.py" backup 2>&1)
if [ $? -eq 0 ]; then
    backup_id=$(echo "$backup_output" | grep "バックアップID:" | sed 's/.*バックアップID: //')
    print_status $GREEN "✅ Backup created: $backup_id"
else
    print_status $YELLOW "⚠️ Backup creation skipped (may already exist)"
fi

# Step 5: File organization
print_status $BLUE "📁 Step 5: Organizing files..."
if python3 "$SCRIPT_DIR/migrate_installer.py" organize; then
    print_status $GREEN "✅ Files organized"
else
    print_status $YELLOW "⚠️ File organization completed with warnings"
fi

# Step 6: Core migration
print_status $BLUE "⚙️ Step 6: Running core migration..."
if python3 "$SCRIPT_DIR/migrate_installer.py" migrate; then
    print_status $GREEN "✅ Core migration completed"
else
    print_status $RED "❌ Core migration failed"
    exit 1
fi

# Step 7: Validation
print_status $BLUE "🧪 Step 7: Running validation..."
if python3 "$SCRIPT_DIR/migration_validator.py" --project-root "$PROJECT_ROOT"; then
    print_status $GREEN "✅ Validation passed"
    validation_success=true
else
    print_status $YELLOW "⚠️ Validation completed with warnings"
    validation_success=false
fi

# Step 8: Final status check
print_status $BLUE "📊 Step 8: Final status check..."
python3 "$SCRIPT_DIR/migrate_installer.py" status | grep -E "(phase|timestamp|completed_steps)" || true

echo ""
print_status $BLUE "=================================="
if [ "$validation_success" = true ]; then
    print_status $GREEN "🎉 MIRRALISM V2 Installation Complete!"
    echo ""
    print_status $GREEN "Next steps:"
    echo "  1. Review any warnings in the validation report"
    echo "  2. Test core functionality with: node scripts/getDate.js"
    echo "  3. Check CLAUDE.md for usage instructions"
    echo ""
    print_status $BLUE "Installation logs: $PROJECT_ROOT/.mirralism/migration_install.log"
else
    print_status $YELLOW "⚠️ Installation completed with warnings"
    echo ""
    print_status $YELLOW "Please review:"
    echo "  1. Validation report in .mirralism/"
    echo "  2. Installation logs for any issues"
    echo "  3. Consider running: python3 scripts/migration_validator.py"
    echo ""
    if [ -n "$backup_id" ]; then
        print_status $BLUE "Rollback available: python3 scripts/migrate_installer.py rollback --backup-id $backup_id"
    fi
fi

print_status $BLUE "=================================="