$ErrorActionPreference='Stop'
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
$doc=$null
try {
  $path=(Resolve-Path 'submission/relay_uas_aeroconf.docx').Path
  $doc=$word.Documents.Open($path,$false,$false)
  foreach($toc in $doc.TablesOfContents){
    $toc.Update()
    $toc.Range.Font.Size=8
    $toc.Range.ParagraphFormat.SpaceAfter=0
    $toc.Range.ParagraphFormat.SpaceBefore=0
  }
  $doc.Save()
  Write-Output ('WORD-PAGES: '+$doc.ComputeStatistics(2))
} finally {
  if($null -ne $doc){$doc.Close(0)}
  $word.Quit()
}
