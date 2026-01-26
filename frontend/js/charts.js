// d3.js visualization functions (d3 is loaded globally from CDN)

function renderMedicationAdherenceTimeline(data, containerId) {
    if (!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">No data to display</p>';
        return;
    }

    const margin = { top: 20, right: 30, bottom: 40, left: 100 };
    const width = 800 - margin.left - margin.right;
    const height = Math.max(400, data.length * 50) - margin.top - margin.bottom;
    
    // Clear container
    d3.select(`#${containerId}`).selectAll("*").remove();
    
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    
    // Parse dates (handle both camelCase and snake_case)
    const parseDate = d3.timeParseISO;
    data.forEach(d => {
        const dateStr = d.effectiveDateTime || d.effective_date_time || '';
        d.date = parseDate(dateStr);
    });
    
    // Get unique medications
    const medications = [...new Set(data.map(d => d.medication?.display || 'Unknown'))];
    
    // Scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(data, d => d.date).filter(d => d != null))
        .range([0, width]);
    
    const yScale = d3.scaleBand()
        .domain(medications)
        .range([0, height])
        .padding(0.2);
    
    // Axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat("%Y-%m-%d %H:%M")));
    
    svg.append("g")
        .call(d3.axisLeft(yScale));
    
    // Add data points
    svg.selectAll(".medication-point")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", "medication-point")
        .attr("cx", d => xScale(d.date) || 0)
        .attr("cy", d => yScale(d.medication?.display || 'Unknown') + yScale.bandwidth() / 2)
        .attr("r", 6)
        .attr("fill", d => {
            const status = d.status?.toLowerCase() || '';
            return status === 'completed' ? "#4CAF50" : status === 'not-taken' ? "#f44336" : "#ff9800";
        })
        .attr("stroke", "#fff")
        .attr("stroke-width", 2)
        .append("title")
        .text(d => {
            const dateStr = d.effectiveDateTime || d.effective_date_time || '';
            const medName = d.medication?.display || 'Unknown';
            const status = d.status || 'unknown';
            return `${medName}\n${dateStr}\nStatus: ${status}`;
        });
}

function renderTemperatureChart(data, containerId) {
    if (!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">No temperature data available</p>';
        return;
    }

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;
    
    d3.select(`#${containerId}`).selectAll("*").remove();
    
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    
    // Filter temperature observations (handle both camelCase and snake_case)
    const tempData = data.filter(d => {
        const code = d.code?.coding?.[0]?.code;
        const hasValue = d.valueQuantity || d.value_quantity;
        return code === '8310-5' && hasValue;
    }).map(d => {
        const dateStr = d.effectiveDateTime || d.effective_date_time || '';
        const value = d.valueQuantity?.value || d.value_quantity?.value || 0;
        return {
            date: d3.timeParseISO(dateStr),
            value: value
        };
    }).filter(d => d.date != null);
    
    if (tempData.length === 0) {
        document.getElementById(containerId).innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">No temperature data available</p>';
        return;
    }
    
    // Scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(tempData, d => d.date))
        .range([0, width]);
    
    const yScale = d3.scaleLinear()
        .domain([Math.max(30, d3.min(tempData, d => d.value) - 2), 
                 Math.min(40, d3.max(tempData, d => d.value) + 2)])
        .range([height, 0]);
    
    // Line generator
    const line = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.value))
        .curve(d3.curveMonotoneX);
    
    // Add line
    svg.append("path")
        .datum(tempData)
        .attr("fill", "none")
        .attr("stroke", "#2196F3")
        .attr("stroke-width", 3)
        .attr("d", line);
    
    // Add data points
    svg.selectAll(".temp-point")
        .data(tempData)
        .enter()
        .append("circle")
        .attr("class", "temp-point")
        .attr("cx", d => xScale(d.date))
        .attr("cy", d => yScale(d.value))
        .attr("r", 4)
        .attr("fill", "#2196F3")
        .append("title")
        .text(d => `Temp: ${d.value.toFixed(1)}°C\n${d3.timeFormat("%Y-%m-%d %H:%M")(d.date)}`);
    
    // Add axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat("%Y-%m-%d %H:%M")));
    
    svg.append("g")
        .call(d3.axisLeft(yScale))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", -40)
        .attr("x", -height / 2)
        .attr("text-anchor", "middle")
        .text("Temperature (°C)");
}

function renderHeartRateChart(data, containerId) {
    if (!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">No heart rate data available</p>';
        return;
    }

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;
    
    d3.select(`#${containerId}`).selectAll("*").remove();
    
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    
    // Filter heart rate observations (handle both camelCase and snake_case)
    const hrData = data.filter(d => {
        const code = d.code?.coding?.[0]?.code;
        const hasValue = d.valueQuantity || d.value_quantity;
        return code === '8867-4' && hasValue;
    }).map(d => {
        const dateStr = d.effectiveDateTime || d.effective_date_time || '';
        const value = d.valueQuantity?.value || d.value_quantity?.value || 0;
        return {
            date: d3.timeParseISO(dateStr),
            value: value
        };
    }).filter(d => d.date != null);
    
    if (hrData.length === 0) {
        document.getElementById(containerId).innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">No heart rate data available</p>';
        return;
    }
    
    // Scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(hrData, d => d.date))
        .range([0, width]);
    
    const yScale = d3.scaleLinear()
        .domain([Math.max(40, d3.min(hrData, d => d.value) - 10), 
                 Math.min(120, d3.max(hrData, d => d.value) + 10)])
        .range([height, 0]);
    
    // Line generator
    const line = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.value))
        .curve(d3.curveMonotoneX);
    
    // Add line
    svg.append("path")
        .datum(hrData)
        .attr("fill", "none")
        .attr("stroke", "#f44336")
        .attr("stroke-width", 3)
        .attr("d", line);
    
    // Add data points
    svg.selectAll(".hr-point")
        .data(hrData)
        .enter()
        .append("circle")
        .attr("class", "hr-point")
        .attr("cx", d => xScale(d.date))
        .attr("cy", d => yScale(d.value))
        .attr("r", 4)
        .attr("fill", "#f44336")
        .append("title")
        .text(d => `HR: ${Math.round(d.value)} bpm\n${d3.timeFormat("%Y-%m-%d %H:%M")(d.date)}`);
    
    // Add axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat("%Y-%m-%d %H:%M")));
    
    svg.append("g")
        .call(d3.axisLeft(yScale))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", -40)
        .attr("x", -height / 2)
        .attr("text-anchor", "middle")
        .text("Heart Rate (bpm)");
}

// Make functions globally available
window.renderMedicationAdherenceTimeline = renderMedicationAdherenceTimeline;
window.renderTemperatureChart = renderTemperatureChart;
window.renderHeartRateChart = renderHeartRateChart;
