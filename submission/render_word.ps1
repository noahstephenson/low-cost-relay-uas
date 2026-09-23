$ErrorActionPreference='Stop'
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
try {
 $path=(Resolve-Path 'submission/relay_uas_aeroconf.docx').Path
 $doc=$word.Documents.Open($path,$false,$false)
 $doc.Fields.Update() | Out-Null
 foreach($toc in $doc.TablesOfContents){$toc.Update()}
 $doc.Repaginate()
 $doc.Save()
 Write-Output ('WORD-PAGES: '+$doc.ComputeStatistics(2))
 $doc.Close(0)
} finally {$word.Quit()}
