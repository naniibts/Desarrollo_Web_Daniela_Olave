// === Gráfico de líneas ===
fetch('/api/estadisticas/dias')
  .then(res => res.json())
  .then(datos => {
    const ctx = document.getElementById('graficoDias');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: datos.map(d => d.dia),
        datasets: [{
          label: 'Cantidad de avisos',
          data: datos.map(d => d.cantidad),
          borderColor: '#738b9c',
          backgroundColor: 'rgba(115,139,156,0.2)',
          fill: true
        }]
      }
    });
  });

// === Gráfico de torta ===
fetch('/api/estadisticas/tipos')
  .then(res => res.json())
  .then(datos => {
    const ctx = document.getElementById('graficoTipos');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: datos.map(d => d.tipo),
        datasets: [{
          data: datos.map(d => d.cantidad),
          backgroundColor: ['#e0b3d9', '#738b9c']
        }]
      }
    });
  });

// === Gráfico de barras ===
fetch('/api/estadisticas/meses')
  .then(res => res.json())
  .then(datos => {
    const ctx = document.getElementById('graficoMeses');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: datos.map(d => d.mes),
        datasets: [
          {
            label: 'Gatos',
            data: datos.map(d => d.gatos),
            backgroundColor: '#e0b3d9'
          },
          {
            label: 'Perros',
            data: datos.map(d => d.perros),
            backgroundColor: '#738b9c'
          }
        ]
      }
    });
  });
