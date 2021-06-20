showFull = () => {
    let blocks = document.querySelectorAll(".notShowDoctor");
    blocks.forEach( e => {
        e.classList.remove("notShowDoctor");
    })
}

showAnalytics = () => {
    let info = document.querySelector(".info");
    let graph = document.querySelector(".graph");
    info.classList.remove("hide");
    graph.classList.remove("hide");
}
