async function loadRepos(){
  try{
    const res = await fetch('../registry/repos.json'); const repos = await res.json();
    const wrap = document.getElementById('repo-cards'); if(!wrap) return;
    wrap.innerHTML='';
    repos.forEach(r=>{
      const el = document.createElement('div'); el.className = 'card';
      el.innerHTML = `
        <h3>${r.name}</h3>
        <p>${r.description||''}</p>
        <div class="links">
          ${r.github?`<a href="${r.github}" target="_blank">GitHub</a>`:''}
          ${r.huggingface?` · <a href="${r.huggingface}" target="_blank">Hugging Face</a>`:''}
          ${r.replit?` · <a href="${r.replit}" target="_blank">Replit</a>`:''}
          ${r.ipfs_cid?` · <a href="https://ipfs.io/ipfs/${r.ipfs_cid}" target="_blank">IPFS</a>`:''}
        </div>`;
      wrap.appendChild(el);
    });
  }catch(e){}
}
loadRepos();
