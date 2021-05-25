window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};


function render_chart(time, cpu_data, gpu_data, memory_data, machine_name) {
    var ctx = document.getElementById('chart_' + machine_name).getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time,
            datasets: [
                {
                    label: "CPU Percentage",
                    backgroundColor: window.chartColors.blue,
                    borderColor: window.chartColors.blue,
                    data: cpu_data,
                    fill: false
                },
                {
                    label: "GPU Percentage",
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
                    data: gpu_data,
                    fill: false
                },
                {
                    label: "Memory Percentage",
                    backgroundColor: window.chartColors.orange,
                    borderColor: window.chartColors.orange,
                    data: memory_data,
                    fill: false
                },

            ]
        },
        options: {
            responsive: 'true',
            title: {
                display: true,
                text: machine_name
            },
        }
    });
}

const data_path = "static/";
let machine_names = [];
$.getJSON("static/machine_names.json", function (data) {
    machine_names = data["names"];
    for (const machine_name of machine_names) {
        let json_file = data_path + machine_name + ".json";
        $.getJSON(json_file, function (data) {
            const time = data.cpu.map(function (e) {
                return e[0];
            });
            const cpu_data = data.cpu.map(function (e) {
                return e[1];
            });

            const gpu_data = data.gpu.map(function (e) {
                return e[0].mem_used_percent;
            });

            const memory_data = data.memory.map(function (e) {
                return e;
            });
            render_chart(time, cpu_data, gpu_data, memory_data, machine_name)
        });
    }
})