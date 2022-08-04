function triggerFileInput(elem) {
    document.querySelector("#uploadValidator").innerHTML = `${elem.files[0].name} (${formatBytes(elem.files[0].size)})`;

    setTimeout(() => {
        document.querySelector("#hidden").style.display = "inline";
    }, 300);
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
}
