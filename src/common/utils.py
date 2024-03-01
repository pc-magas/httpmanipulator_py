
def convertDomainIntoWildcard(domain):
    parts=domain.split(".")
    if(len(parts)>=3 and parts[0]!="*"):
        parts[0]="*"
        return ".".join(parts)

    return "*".domain