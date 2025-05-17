<template>
  <div>
    <button @click="downloadChart" class="download-btn material-icons download" title="Download as image"></button>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch  } from 'vue';
import { Chart, registerables } from 'chart.js';
import type { ChartType } from 'chart.js';
import type { PropType } from 'vue';

Chart.register(...registerables);

export default defineComponent({
  name: 'GraphChart',
  props: {
    plotType: {
      type: String as PropType<ChartType>,
      required: true,
    },
    labels: {
      type: Array as () => string[],
      required: true,
    },
    data: {
      type: Array as () => number[],
      required: true,
    },
    title: {
      type: String,
      required: false,
      default: 'Data visualization',
    },
    xAxisLabel: {
      type: String,
      required: false,
      default: 'X Axis',
    },
    yAxisLabel: {
      type: String,
      required: false,
      default: 'Y Axis',
    },
  },
  setup(props) {
    const chartCanvas = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    const renderChart = () => {
      if (chartInstance) {
        chartInstance.destroy();
      }

      if (chartCanvas.value) {
        chartInstance = new Chart(chartCanvas.value, {
          type: props.plotType,
          data: {
            labels: props.labels,
            datasets: [
              {
                data: props.data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: props.title, // Plot title
                font: {
                  size: 18,
                },
              },
              legend: {
              display: false,
            }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: props.xAxisLabel, // X-axis label
                  font: {
                    size: 14,
                  },
                },
              },
              y: {
                title: {
                  display: true,
                  text: props.yAxisLabel, // Y-axis label
                  font: {
                    size: 14,
                  },
                },
              },
            },

          },
        });
      }
    };

    const downloadChart = () => {
      if (chartInstance && chartCanvas.value) {
        const link = document.createElement('a');
        link.href = chartInstance.toBase64Image();
        link.download = 'chart.png';
        link.click();
      }
    };

    onMounted(renderChart);
    watch(() => [props.plotType, props.labels, props.data], renderChart);

    return {
      chartCanvas,
      downloadChart,
    };
  },
});
</script>

<style scoped>
div {
  position: relative;
  height: 400px;
  width: 100%;
}

canvas {
  padding-bottom: 40px;
}

.download-btn {
  font-size: 16px;
  float: right;
  margin-top: 10px;
  margin-right: 10px;
  padding: 4px 6px;
  color: var(--color-block-dark);
  background-color: white;
  border: 1px solid;
  border-radius: 4px;
  border-color: var(--color-block);
  cursor: pointer;
}

.download-btn:hover {
  background-color: var(--color-block);
  transition: background-color 0.5s ease;
}
</style>
