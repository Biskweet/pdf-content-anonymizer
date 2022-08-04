function triggerFileInput(elem) {
    let submitButton = document.querySelector("#hidden input");

    if (elem.files.length == 0) return;

    if ((elem.files.length == 1 && elem.files[0].name.slice(-4).toUpperCase() == ".PDF") || elem.files.length > 1) {
        if (elem.files.length == 1) {
            document.querySelector("#uploadValidator").innerHTML = `${elem.files[0].name} (${formatBytes(elem.files[0].size)})`;
        } else {
            document.querySelector("#uploadValidator").innerHTML = elem.files.length + " files selected";
        }

        submitButton.disabled = false;
        submitButton.style.backgroundColor = "#710d02";  // Base red
        submitButton.style.color = "#f6f2f2";            // Base pink
        submitButton.style.cursor = "pointer";
    } else {
        document.querySelector("#uploadValidator").innerHTML = "File type isn't PDF!";
        submitButton.disabled = true;
        submitButton.style.backgroundColor = "#b28a85";  // Greyed red
        submitButton.style.color = "#d3b5b5";            // Greyed pink
        submitButton.style.cursor = "default";
    }

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
