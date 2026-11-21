$root = "C:\Users\abdel\OneDrive\Documents\Default Project\rocket_game_v2"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8766/")
$listener.Start()
Write-Output "V2_SERVER_READY http://localhost:8766/"
while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $path = $ctx.Request.Url.AbsolutePath.TrimStart('/')
  if ($path -eq '') { $path = 'index.html' }
  $file = Join-Path $root $path
  if (Test-Path $file -PathType Leaf) {
    $bytes = [System.IO.File]::ReadAllBytes($file)
    switch -Regex ($file) {
      '\.html$' { $ctx.Response.ContentType = 'text/html; charset=utf-8' }
      '\.js$'   { $ctx.Response.ContentType = 'text/javascript; charset=utf-8' }
      '\.glb$'  { $ctx.Response.ContentType = 'model/gltf-binary' }
      default   { $ctx.Response.ContentType = 'application/octet-stream' }
    }
    $ctx.Response.ContentLength64 = $bytes.Length
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
  } else { $ctx.Response.StatusCode = 404 }
  $ctx.Response.Close()
}
