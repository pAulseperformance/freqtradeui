function addArguments() {
    var commands = document.getElementById("commands");
    function getSelectedOption(sel) {
        var opt;
        for (var i = 0, len = sel.options.length; i < len; i++) {
            opt = sel.options[i];
            if (opt.selected === true) {
                break;
            }
        }

        switch (opt.value) {
            case 'forcesell':
                document.getElementById('command-args').style.display = "block";
                document.getElementById('command-args').value = 'tradeid';
                break;
            case 'forcebuy':
                document.getElementById('command-args').style.display = "block";
                document.getElementById('command-args').value = 'BTC/USDT,1';
                break;
            case 'daily':
                document.getElementById('command-args').style.display = "block";
                document.getElementById('command-args').value = 7;
                break;
            case 'blacklist':
                document.getElementById('command-args').style.display = "block";
                document.getElementById('command-args').value = 'BCC/USDT';
                break;
            default:
                document.getElementById('command-args').style.display = "none";
        }

    }
    getSelectedOption(commands);
}

// var myLineChart = new Chart(ctx, {
//     type: 'line',
//     data: data,
//     options: options
// });

