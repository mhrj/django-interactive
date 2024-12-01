import re

def validate_script(r_script):
    """
    Checks for destructive or unsafe R commands in the script.
    """
    # List of forbidden keywords and their dangerous usage patterns
    forbidden_patterns = [
        r'\bunlink\(',       # Prevent deletion of files
        r'\bsystem\(',       # Prevent system calls
        r'\brm\(',           # Prevent removal of variables/files
        r'\bquit\(',         # Prevent quitting the R session
        r'\bshutdown\(',     # Prevent shutting down the system
        r'\bfile.remove\('   # Prevent file removals
    ]

    # Whitelisted keywords or usage patterns
    allowed_patterns = [
        r'\bpng\(',          # Allow generating PNG plots
        r'\bggsave\('        # Allow saving plots using ggsave
    ]

    # Check for forbidden patterns
    for pattern in forbidden_patterns:
        if re.search(pattern, r_script, re.IGNORECASE):
            # Ensure it’s not part of an allowed pattern
            for allowed in allowed_patterns:
                if re.search(allowed, r_script, re.IGNORECASE):
                    break
            else:
                return False

    return True
