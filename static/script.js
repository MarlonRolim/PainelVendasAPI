function faszGet(url){
    let request = new XMLHttpRequest()
    request.open("GET",url, false)
    request.send()
    return request.responseText
}

function atualizar() {
    data = faszGet("/api/painelvendasav/volumedia")
    data = JSON.parse(data)
    document.querySelector("#volume-total-text").replaceChildren(data["vTT"])
    document.querySelector("#volume-total-falta-text").replaceChildren(data["vTTcf"])
    document.querySelector("#falta-total-text").replaceChildren(data["vTTf"])
    document.querySelector("#volume-cerveja-text").replaceChildren(data["vC"])
    document.querySelector("#volume-cerveja-falta-text").replaceChildren(data["vCcf"])
    document.querySelector("#falta-cerveja-text").replaceChildren(data["vCf"])
    document.querySelector("#volume-nab-text").replaceChildren(data["vN"])
    document.querySelector("#volume-nab-falta-text").replaceChildren(data["vNcf"])
    document.querySelector("#falta-nab-text").replaceChildren(data["vNf"])
    document.querySelector("#volume-rgb-text").replaceChildren(data["vR"])
    document.querySelector("#volume-rgb-falta-text").replaceChildren(data["vRcf"])
    document.querySelector("#falta-rgb-text").replaceChildren(data["vRf"])
    document.querySelector("#volume-heco-text").replaceChildren(data["vH"])
    document.querySelector("#volume-heco-falta-text").replaceChildren(data["vHcf"])
    document.querySelector("#falta-heco-text").replaceChildren(data["vHf"])
    document.querySelector("#volume-pm-text").replaceChildren(data["vP"])
    document.querySelector("#volume-pm-falta-text").replaceChildren(data["vPcf"])
    document.querySelector("#falta-pm-text").replaceChildren(data["vPf"])
   
}

$(function() {
    setTime();
    function setTime() {
       var date = new Date().getTime();
       
       setTimeout(setTime, 60000);
       atualizar()
    }
  });

  