var line_bind_btn=document.getElementById("line_bind1")
var url_domain=window.location.host

line_bind_btn.setAttribute('href','https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=damgGNEOW7TW6vBtxoCWtt&redirect_uri=http://'+url_domain+'/line_notify_bind&scope=notify&state=NO_STATE')
console.log(url_domain)