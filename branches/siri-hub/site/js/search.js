async function setupSearch(){
  const q = document.getElementById('q'); const out = document.getElementById('searchOut') || document.getElementById('out');
  let data = [];
  try{
    const r = await fetch('data/ko-registry.json'); data = await r.json();
  }catch(e){ if(out) out.textContent='No KO registry yet. You can still create a new KO below.'; return; }
  const render = list => { if(out) out.textContent = JSON.stringify(list, null, 2); };
  render(data);
  if(q) q.addEventListener('input', ()=>{
    const s = q.value.toLowerCase();
    render(data.filter(x => JSON.stringify(x).toLowerCase().includes(s)));
  });
}
setupSearch();
