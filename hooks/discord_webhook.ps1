$webhookUrl = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

$payload = @{
  username = "Grok Crypto Sentinel"
  content  = "**📡 Signal Alert – $(Get-Date -Format "yyyy-MM-dd HH:mm")**`n🧠 Stay alert.`n📉 New market signal detected."
}

Invoke-RestMethod -Uri $webhookUrl -Method Post -Body ($payload | ConvertTo-Json -Depth 2) -ContentType 'application/json'
