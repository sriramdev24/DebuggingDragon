// Campus Knowledge Network Visual Graph with Vis.js

let network = null;
let allNodes = [];
let allEdges = [];
let nodesDataSet = null;
let edgesDataSet = null;

document.addEventListener("DOMContentLoaded", function () {
  initNetworkGraph();
});

function initNetworkGraph() {
  const container = document.getElementById("network-graph-canvas");
  if (!container) return;

  // Show loading indicator
  const loadingEl = document.getElementById("graph-loading");
  if (loadingEl) loadingEl.style.display = "flex";

  fetch("/api/network-data")
    .then(res => res.json())
    .then(data => {
      allNodes = data.nodes;
      allEdges = data.edges;

      nodesDataSet = new vis.DataSet(allNodes);
      edgesDataSet = new vis.DataSet(allEdges);

      const graphData = {
        nodes: nodesDataSet,
        edges: edgesDataSet
      };

      const options = {
        nodes: {
          borderWidth: 2,
          size: 20,
          font: {
            color: "#0f172a",
            size: 13,
            face: "Plus Jakarta Sans, sans-serif"
          },
          shadow: {
            enabled: true,
            color: "rgba(15,23,42,0.15)",
            size: 6,
            x: 2,
            y: 2
          }
        },
        edges: {
          smooth: {
            type: "continuous",
            roundness: 0.2
          },
          arrows: {
            to: { enabled: true, scaleFactor: 0.6 }
          },
          font: {
            strokeWidth: 2,
            strokeColor: "#ffffff",
            color: "#0f172a",
            size: 10,
            face: "Plus Jakarta Sans, sans-serif"
          }
        },
        physics: {
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -50,
            centralGravity: 0.01,
            springLength: 100,
            springConstant: 0.08,
            damping: 0.4
          },
          stabilization: {
            iterations: 150,
            updateInterval: 25
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 150,
          hideEdgesOnDrag: true,
          zoomView: true
        }
      };

      network = new vis.Network(container, graphData, options);

      if (loadingEl) loadingEl.style.display = "none";

      // On Node Click -> Open Inspector Drawer
      network.on("click", function (params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          handleNodeSelection(nodeId);
        }
      });

      // Update counters
      updateGraphStats(data.nodes.length, data.edges.length);
    })
    .catch(err => {
      console.error("Failed to load network graph data:", err);
      if (loadingEl) {
        loadingEl.innerHTML = `<span class="text-rose-400">Failed to load graph data. Please refresh.</span>`;
      }
    });
}

function updateGraphStats(totalNodes, totalEdges) {
  const nodeCountEl = document.getElementById("graph-node-count");
  const edgeCountEl = document.getElementById("graph-edge-count");
  if (nodeCountEl) nodeCountEl.innerText = totalNodes;
  if (edgeCountEl) edgeCountEl.innerText = totalEdges;
}

function handleNodeSelection(nodeId) {
  const drawer = document.getElementById("node-drawer");
  if (!drawer) return;

  if (nodeId.startsWith("user_")) {
    // Student Node selected
    fetch(`/api/user/${nodeId}`)
      .then(res => res.json())
      .then(user => {
        renderStudentDrawer(user);
        drawer.classList.remove("translate-x-full");
      });
  } else if (nodeId.startsWith("skill_")) {
    // Skill Node selected
    const skillNode = allNodes.find(n => n.id === nodeId);
    renderSkillDrawer(skillNode, nodeId);
    drawer.classList.remove("translate-x-full");
  }
}

function closeDrawer() {
  const drawer = document.getElementById("node-drawer");
  if (drawer) drawer.classList.add("translate-x-full");
}

function renderStudentDrawer(user) {
  const container = document.getElementById("drawer-content");
  if (!container) return;

  const offeredHtml = (user.skills_offered || []).map(s => `
    <div class="p-3 rounded-2xl bg-[#dcfce7] border-2 border-slate-900 text-xs font-bold shadow-[2px_2px_0px_0px_#0f172a]">
      <div class="flex items-center justify-between">
        <span class="text-slate-900">${s.name}</span>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-white border border-slate-900">${s.level}</span>
      </div>
      <div class="text-[11px] text-slate-700 mt-1 font-medium">${s.experience || 'Experienced mentor'}</div>
    </div>
  `).join('');

  const wantedHtml = (user.skills_wanted || []).map(s => `
    <div class="p-3 rounded-2xl bg-[#f3e8ff] border-2 border-slate-900 text-xs font-bold shadow-[2px_2px_0px_0px_#0f172a]">
      <div class="flex items-center justify-between">
        <span class="text-slate-900">${s.name}</span>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-white border border-slate-900">${s.target_level || 'Goal'}</span>
      </div>
      <div class="text-[11px] text-slate-700 mt-1 italic font-medium">${s.goal || 'Goal to learn'}</div>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="space-y-4 text-xs font-bold text-slate-800">
      <div class="flex items-center gap-3">
        <img src="${user.avatar}" class="w-14 h-14 rounded-full object-cover border-2 border-slate-900 shadow-[2px_2px_0px_0px_#0f172a]">
        <div>
          <h3 class="font-display font-black text-slate-900 text-base">${user.name}</h3>
          <div class="text-slate-600 text-[11px]">${user.department} &bull; ${user.year}</div>
          <div class="text-slate-900 font-extrabold mt-0.5">
            ⭐ ${user.rating} &bull; ${user.karma_points} Points
          </div>
        </div>
      </div>

      <p class="text-slate-700 italic p-3 rounded-2xl bg-[#faf8f5] border-2 border-slate-900 font-medium">
        "${user.bio}"
      </p>

      <div>
        <div class="text-[10px] font-black uppercase text-emerald-900 tracking-wider mb-2">Can Teach (Offered):</div>
        <div class="space-y-2">${offeredHtml || '<div class="text-slate-500">No skills listed</div>'}</div>
      </div>

      <div>
        <div class="text-[10px] font-black uppercase text-purple-900 tracking-wider mb-2">Wants to Learn:</div>
        <div class="space-y-2">${wantedHtml || '<div class="text-slate-500">No goals listed</div>'}</div>
      </div>

      <div class="pt-2 border-t-2 border-slate-900 space-y-2">
        <a href="/switch-user/${user._id}" class="w-full py-2.5 rounded-full text-xs font-extrabold bg-[#fef08a] hover:bg-[#fde047] text-slate-900 border-2 border-slate-900 flex items-center justify-center gap-2 shadow-[2px_2px_0px_0px_#0f172a]">
          Switch Identity to this Student
        </a>
        <a href="/matches" class="w-full py-2.5 rounded-full text-xs font-extrabold bg-slate-900 hover:bg-slate-800 text-white flex items-center justify-center gap-2">
          Match DNA & Barter
        </a>
      </div>
    </div>
  `;
}

function renderSkillDrawer(skillNode, nodeId) {
  const container = document.getElementById("drawer-content");
  if (!container) return;

  const teachers = allEdges
    .filter(e => e.to === nodeId && e.from.startsWith("user_"))
    .map(e => allNodes.find(n => n.id === e.from))
    .filter(Boolean);

  const learners = allEdges
    .filter(e => e.to === nodeId && e.from.startsWith("user_") && e.label === "Wants")
    .map(e => allNodes.find(n => n.id === e.from))
    .filter(Boolean);

  container.innerHTML = `
    <div class="space-y-4 text-xs font-bold text-slate-800">
      <div class="p-4 rounded-2xl bg-[#fef08a] border-2 border-slate-900 shadow-[2px_2px_0px_0px_#0f172a]">
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-white border border-slate-900 uppercase">Skill Node</span>
        <h3 class="font-display font-black text-lg text-slate-900 mt-1">${skillNode.label}</h3>
        <div class="text-slate-700 text-[11px]">Category: <strong>${skillNode.category || 'General'}</strong></div>
      </div>

      <div>
        <div class="text-[10px] font-black uppercase text-emerald-900 tracking-wider mb-2">Available Mentors (${teachers.length}):</div>
        <div class="space-y-2">
          ${teachers.map(t => `
            <a href="/switch-user/${t.id}" class="p-2.5 rounded-2xl bg-white border-2 border-slate-900 flex items-center gap-2.5 hover:bg-[#dcfce7] transition-colors shadow-[2px_2px_0px_0px_#0f172a]">
              <img src="${t.avatar}" class="w-7 h-7 rounded-full object-cover border border-slate-900">
              <span class="text-slate-900 font-extrabold">${t.label}</span>
            </a>
          `).join('') || '<div class="text-slate-500">None currently listed</div>'}
        </div>
      </div>

      <div>
        <div class="text-[10px] font-black uppercase text-purple-900 tracking-wider mb-2">Students Seeking This (${learners.length}):</div>
        <div class="space-y-2">
          ${learners.map(l => `
            <div class="p-2.5 rounded-2xl bg-white border-2 border-slate-900 flex items-center gap-2.5 shadow-[2px_2px_0px_0px_#0f172a]">
              <img src="${l.avatar}" class="w-7 h-7 rounded-full object-cover border border-slate-900">
              <span class="text-slate-900 font-extrabold">${l.label}</span>
            </div>
          `).join('') || '<div class="text-slate-500">No active students seeking this</div>'}
        </div>
      </div>
    </div>
  `;
}

// Graph filter by category
function filterGraphCategory(cat) {
  if (!nodesDataSet) return;

  if (!cat || cat === 'all') {
    nodesDataSet.clear();
    nodesDataSet.add(allNodes);
    edgesDataSet.clear();
    edgesDataSet.add(allEdges);
    return;
  }

  // Filter skills matching category and connected users
  const filteredSkillNodes = allNodes.filter(n => n.group === 'skill' && n.category === cat);
  const skillIds = new Set(filteredSkillNodes.map(s => s.id));

  const relevantEdges = allEdges.filter(e => skillIds.has(e.to));
  const userIds = new Set(relevantEdges.map(e => e.from));

  const filteredUserNodes = allNodes.filter(n => userIds.has(n.id));

  nodesDataSet.clear();
  nodesDataSet.add([...filteredUserNodes, ...filteredSkillNodes]);

  edgesDataSet.clear();
  edgesDataSet.add(relevantEdges);

  if (network) network.fit();
}

// Search student or skill
function searchGraph(query) {
  if (!query || !nodesDataSet) return;
  const q = query.toLowerCase().trim();
  const found = allNodes.find(n => n.label && n.label.toLowerCase().includes(q));

  if (found && network) {
    network.focus(found.id, {
      scale: 1.2,
      animation: { duration: 800, easingFunction: "easeInOutQuad" }
    });
    handleNodeSelection(found.id);
  }
}

// Zoom / View Controls
function resetGraphView() {
  if (network) network.fit({ animation: { duration: 600 } });
}

function zoomGraph(factor) {
  if (!network) return;
  const scale = network.getScale();
  network.moveTo({ scale: scale * factor });
}

function toggleGraphPhysics() {
  if (!network) return;
  const curr = network.physics.options.enabled;
  network.setOptions({ physics: { enabled: !curr } });
}
