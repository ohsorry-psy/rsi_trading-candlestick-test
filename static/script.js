function generateChart() {
  const symbol = document.getElementById('ticker').value;
  const start = document.getElementById('start').value;
  const end = document.getElementById('end').value;

  const formData = new URLSearchParams();
  formData.append('symbol', symbol);
  formData.append('start', start);
  formData.append('end', end);

  fetch('/generate', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    if (data.status === 'ok') {
      document.getElementById('chart').src = data.image_url + '?t=' + new Date().getTime();
    } else {
      alert('❌ 차트 생성 실패: ' + data.message);
    }
  })
  .catch(error => {
    alert('🚨 오류 발생: ' + error);
  });
}


  
  