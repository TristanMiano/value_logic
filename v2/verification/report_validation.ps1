# Validation of a completed child's report must not erase a failed attempt.
# This helper never executes report content. Callers retain stdout/stderr,
# exit status and retry limits independently of this shallow identity check.
function Test-F12Report {
    param([Parameter(Mandatory=$true)][string]$Path,
          [Parameter(Mandatory=$true)][System.Collections.IDictionary]$Expected)
    try {
        $report=Get-Content -LiteralPath $Path -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
        if($null -eq $report -or $report -isnot [pscustomobject]) {
            return [pscustomobject]@{valid=$false; error='Report must be a JSON object.'}
        }
        foreach($field in $Expected.Keys) {
            $property=$report.psobject.Properties[$field]
            if($null -eq $property -or $null -eq $property.Value -or
               $property.Value.GetType() -ne $Expected[$field].GetType() -or
               $property.Value -cne $Expected[$field]) {
                # ConvertFrom-Json returns Int64 for integral JSON values;
                # permit Int32 expectations without accepting strings/bools.
                $integerMatch=($null -ne $property -and
                    ($property.Value -is [int] -or $property.Value -is [long]) -and
                    ($Expected[$field] -is [int] -or $Expected[$field] -is [long]) -and
                    $property.Value -eq $Expected[$field])
                if(-not $integerMatch) {
                    return [pscustomobject]@{valid=$false; error="Report identity mismatch: $field"}
                }
            }
        }
        return [pscustomobject]@{valid=$true; error=$null}
    } catch {
        return [pscustomobject]@{valid=$false; error=$_.Exception.Message}
    }
}
