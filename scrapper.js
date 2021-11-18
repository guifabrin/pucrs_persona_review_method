var links = [...document.querySelectorAll('span')].filter(span=>span.innerText==='[PDF]').map(span=>span.parentElement.href).filter(url=>url)
function downloadObjectAsJson(exportObj, exportName){
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}
downloadObjectAsJson(links, 'links_'+document.querySelector('b.gs_nma').innerText);
[...document.querySelectorAll('a.gs_nma')].filter(item=>item.innerText*1>document.querySelector('b.gs_nma').innerText*1)[0].click()