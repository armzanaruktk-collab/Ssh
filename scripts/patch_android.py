from pathlib import Path

app = Path("app/src/main/java/com/godarmx/ssh/ui/App.kt")
if app.exists():
    text = app.read_text()
    old = "Card(\n                    Modifier.fillMaxWidth(), onClick = { onUse(p) },"
    new = "Card(\n                    onClick = { onUse(p) }, modifier = Modifier.fillMaxWidth(),"
    if old in text:
        app.write_text(text.replace(old, new, 1))
        print("Fixed Material3 Card argument order")
    else:
        print("Card argument pattern not found; leaving source unchanged")

service = Path("app/src/main/java/com/godarmx/ssh/vpn/SshTunnelService.kt")
if service.exists():
    text = service.read_text()
    if "sslFactory(insecure)" in text and "private fun sslFactory(" not in text:
        marker = "    /** Plain HTTP CONNECT through a proxy"
        helper = """    private fun sslFactory(insecure: Boolean): SSLSocketFactory {
        val context = SSLContext.getInstance("TLS")
        val trustManagers: Array<javax.net.ssl.TrustManager>? =
            if (insecure) arrayOf(object : X509TrustManager {
                override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
                override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
                override fun getAcceptedIssuers(): Array<X509Certificate> = emptyArray()
            }) else null
        context.init(null, trustManagers, SecureRandom())
        return context.socketFactory
    }

"""
        if marker not in text:
            raise SystemExit("Could not find insertion point for sslFactory()")
        service.write_text(text.replace(marker, helper + marker, 1))
        print("Added missing sslFactory() implementation")
