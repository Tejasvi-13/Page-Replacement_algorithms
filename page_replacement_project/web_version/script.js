function parseInput() {
    const pages = document.getElementById('pages').value.trim().split(/\s+/).map(Number);
    const frameSize = parseInt(document.getElementById('frameSize').value);
    return [pages, frameSize];
  }
  
  function fifo(pages, frameSize) {
    let memory = [], queue = [], faults = 0;
    pages.forEach(page => {
      if (!memory.includes(page)) {
        faults++;
        if (memory.length < frameSize) {
          memory.push(page);
          queue.push(page);
        } else {
          let removed = queue.shift();
          memory.splice(memory.indexOf(removed), 1);
          memory.push(page);
          queue.push(page);
        }
      }
    });
    return faults;
  }
  
  function lru(pages, frameSize) {
    let memory = [], recent = {}, faults = 0;
    pages.forEach((page, i) => {
      if (!memory.includes(page)) {
        faults++;
        if (memory.length < frameSize) {
          memory.push(page);
        } else {
          const oldest = memory.reduce((a, b) => (recent[a] < recent[b] ? a : b));
          memory.splice(memory.indexOf(oldest), 1);
          memory.push(page);
        }
      }
      recent[page] = i;
    });
    return faults;
  }
  
  function optimal(pages, frameSize) {
    let memory = [], faults = 0;
    for (let i = 0; i < pages.length; i++) {
      let page = pages[i];
      if (!memory.includes(page)) {
        faults++;
        if (memory.length < frameSize) {
          memory.push(page);
        } else {
          let future = memory.map(p => {
            let idx = pages.slice(i + 1).indexOf(p);
            return idx === -1 ? Infinity : idx;
          });
          let toRemove = memory[future.indexOf(Math.max(...future))];
          memory.splice(memory.indexOf(toRemove), 1);
          memory.push(page);
        }
      }
    }
    return faults;
  }
  
  function simulate() {
    const [pages, frameSize] = parseInput();
    if (!pages.length || isNaN(frameSize) || frameSize <= 0) {
      alert("Please enter valid input!");
      return;
    }
  
    const fifoFaults = fifo(pages, frameSize);
    const lruFaults = lru(pages, frameSize);
    const optimalFaults = optimal(pages, frameSize);
  
    document.getElementById('resultText').innerHTML = `
      <strong>Page Faults:</strong><br>
      FIFO: ${fifoFaults}<br>
      LRU: ${lruFaults}<br>
      Optimal: ${optimalFaults}
    `;
  
    const ctx = document.getElementById('myChart').getContext('2d');
    if (window.bar) window.bar.destroy();  // Destroy previous chart
  
    window.bar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['FIFO', 'LRU', 'Optimal'],
        datasets: [{
          label: 'Page Faults',
          data: [fifoFaults, lruFaults, optimalFaults],
          backgroundColor: ['blue', 'green', 'orange']
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      }
    });
  }
  