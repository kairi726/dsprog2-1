// weather_core.js
function getIconByCode(code) {
    const c = String(code);
    if (c.startsWith('4')) return '雪.png';
    if (c.startsWith('3')) return '雨.png';
    if (c === '101' || c === '110' || c === '201') return '晴れand曇り.png';
    if (c === '202') return '曇りand雨.png';
    if (c.startsWith('1')) return '晴れ.png';
    if (c.startsWith('2')) return '曇り.png';
    return '曇り.png';
}

async function loadWeatherFromDB(areaCode) {
    try {
        const response = await fetch(`http://127.0.0.1:5001/weather/${areaCode}`);
        const data = await response.json();
        const container = document.getElementById('weather-container');
        container.innerHTML = ""; 

        data.forEach(item => {
            const d = new Date(item.forecast_date);
            const displayDate = `${d.getMonth() + 1}/${d.getDate()}`;
            const icon = getIconByCode(item.weather_code);

            const card = document.createElement('div');
            card.className = 'weather-card';
            card.innerHTML = `
                <div class="date">${displayDate}</div>
                <div class="weather-text">予報</div>
                <img src="${icon}" alt="天気">
                <div class="details">
                    <span class="temp-max">${item.temp_max}℃</span> / <span class="temp-min">${item.temp_min}℃</span>
                </div>
                <div class="precip">降水確率 ${item.pop}%</div>
            `;
            container.appendChild(card);
        });
    } catch (e) {
        console.error("DB読み込みエラー:", e);
    }
}