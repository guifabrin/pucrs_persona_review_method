function qtext(item, query, text) {
    return [...item.querySelectorAll(query)].filter(span => span.innerText && span.innerText.indexOf(text) > -1)
}

results = [];
promises = [];
[...document.querySelectorAll('span')].filter(span => span.innerText === '[PDF]').filter((value, index, self) => self.indexOf(value) === index).map(span => span.closest('.gs_r')).map(root => {
    console.log(root.getAttribute('data-cid'))
    promises.push(fetch(`https://scholar.google.com.br/scholar?q=info:${root.getAttribute('data-cid')}:scholar.google.com/&output=cite&scirp=0&hl=pt-BR`).then(response => response.text()).then(text => {
        try {
            var wrapper = document.createElement('div');
            wrapper.innerHTML = text;
            var cited = qtext(root, 'a', 'Citado por')[0]
            var splited = root.querySelector('.gs_a').innerText.split(',')
            results.push({
                title: root.querySelector('.gs_rt').innerText,
                url: root.querySelector('.gs_ctg2').parentElement.href,
                cited_by: cited ? cited.innerText.replace(/\D/g, "") * 1 : 0,
                citation: wrapper.querySelector('a').href,
                year: splited[splited.length - 1].split('-')[0] * 1
            })
        } catch (e){
            console.error(e)
        }
    }))
})

function downloadObjectAsJson(exportObj, exportName) {
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

Promise.all(promises).then((values) => {
    downloadObjectAsJson(results, 'links_' + document.querySelector('b.gs_nma').innerText);
    [...document.querySelectorAll('a.gs_nma')].filter(item => item.innerText * 1 > document.querySelector('b.gs_nma').innerText * 1)[0].click()
});