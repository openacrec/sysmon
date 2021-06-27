window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};


function render_chart(data_json) {
    const ctx = document.getElementById('chart_' + data_json["name"]).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_json["time"],
            datasets: [
                {
                    label: "CPU Percentage",
                    backgroundColor: window.chartColors.blue,
                    borderColor: window.chartColors.blue,
                    data: data_json["cpu"],
                    fill: false
                },
                {
                    label: "Memory Percentage",
                    backgroundColor: window.chartColors.orange,
                    borderColor: window.chartColors.orange,
                    data: data_json["memory"],
                    fill: false
                },
                {
                    label: "GPU Percentage",
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
                    data: data_json["gpu"],
                    fill: false
                },
            ]
        },
        options: {
            title: {
                display: true,
                text: data_json["name"]
            }
        }
    });
}
