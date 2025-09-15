function slug(s){return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'')}
async function createPR(){
  const repo = document.getElementById('repo').value.trim();
  const base = document.getElementById('base').value.trim() || 'main';
  const token = document.getElementById('token').value.trim();
  const title = document.getElementById('title').value.trim();
  const kind = document.getElementById('kind').value;
  const authors = document.getElementById('authors').value.split(',').map(s=>s.trim()).filter(Boolean);
  const license = document.getElementById('license').value.trim() || 'CC-BY-SA-4.0';
  const sources = document.getElementById('sources').value.split(',').map(s=>s.trim()).filter(Boolean);
  const tags = document.getElementById('tags').value.split(',').map(s=>s.trim()).filter(Boolean);
  const out = document.getElementById('out');
  if(!repo || !token || !title){ out.textContent='Repo, token, and title are required.'; return; }

  const [owner,name] = repo.split('/');
  const koId = 'ko-' + slug(title);
  const branch = `ko/add-${slug(title)}`;
  const path = `ko/proposals/${koId}.json`;

  const ko = {
    id: koId, title, kind, version: "v1.0.0", authors, license,
    hash: "CID_PLACEHOLDER",
    provenance: { sources, signatures: [], timestamp: new Date().toISOString() },
    tags, moderation: ["research-safe"]
  };
  const body = JSON.stringify(ko, null, 2);

  try{
    // base ref SHA
    let r = await fetch(`https://api.github.com/repos/${owner}/${name}/git/ref/heads/${base}`,
      { headers: { Authorization: `token ${token}`, Accept: 'application/vnd.github+json' } });
    if(!r.ok){ throw new Error('Cannot read base branch: ' + await r.text()); }
    const ref = await r.json(); const sha = ref.object.sha;

    // create branch
    r = await fetch(`https://api.github.com/repos/${owner}/${name}/git/refs`, {
      method: 'POST',
      headers: { Authorization: `token ${token}`, Accept: 'application/vnd.github+json' },
      body: JSON.stringify({ ref: `refs/heads/${branch}`, sha })
    });
    if(!r.ok){ throw new Error('Branch create failed: ' + await r.text()); }

    // commit file
    r = await fetch(`https://api.github.com/repos/${owner}/${name}/contents/${encodeURIComponent(path)}`, {
      method: 'PUT',
      headers: { Authorization: `token ${token}`, Accept: 'application/vnd.github+json' },
      body: JSON.stringify({ message: `ko: add ${koId}`, content: btoa(unescape(encodeURIComponent(body))), branch })
    });
    if(!r.ok){ throw new Error('File commit failed: ' + await r.text()); }

    // open PR
    r = await fetch(`https://api.github.com/repos/${owner}/${name}/pulls`, {
      method: 'POST',
      headers: { Authorization: `token ${token}`, Accept: 'application/vnd.github+json' },
      body: JSON.stringify({ title: `Add KO: ${title}`, head: branch, base, body: "Created via SIRI Copilot" })
    });
    if(!r.ok){ throw new Error('PR creation failed: ' + await r.text()); }
    const pr = await r.json();
    out.textContent = '✅ PR created: ' + pr.html_url + '\n\n' + JSON.stringify(ko, null, 2);
  }catch(e){
    out.textContent = '❌ ' + e.message;
  }
}
document.addEventListener('DOMContentLoaded', ()=>{
  const btn = document.getElementById('make');
  if(btn) btn.addEventListener('click', createPR);
});
