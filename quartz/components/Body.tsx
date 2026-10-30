import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const authScript = `
(function() {
  var KEY = "dml_vapor_access_v1";
  var CODES = ["DML2026", "DML-VAPOR", "DML"];
  function syncAuth() {
    var ok = false;
    try { ok = localStorage.getItem(KEY) === "authorized"; } catch (e) {}
    if (ok) {
      document.documentElement.setAttribute("data-dml-auth", "granted");
    } else {
      document.documentElement.removeAttribute("data-dml-auth");
    }
  }
  syncAuth();
  if (!window.__dmlAuthBound) {
    window.__dmlAuthBound = true;
    document.addEventListener("nav", syncAuth);
    document.addEventListener("submit", function(e) {
      var form = e.target;
      if (!form || form.id !== "dml-access-form") return;
      e.preventDefault();
      var input = document.getElementById("dml-access-input");
      var err = document.getElementById("dml-access-error");
      var val = (input ? input.value : "").trim().toUpperCase();
      if (CODES.indexOf(val) !== -1) {
        try { localStorage.setItem(KEY, "authorized"); } catch (ex) {}
        if (err) err.style.display = "none";
        if (input) input.value = "";
        syncAuth();
      } else {
        if (err) err.style.display = "block";
        if (input) { input.value = ""; input.focus(); }
      }
    });
    document.addEventListener("click", function(e) {
      var btn = e.target && e.target.closest ? e.target.closest("#dml-logout-btn") : null;
      if (!btn) return;
      e.preventDefault();
      try { localStorage.removeItem(KEY); } catch (ex) {}
      syncAuth();
    });
  }
})();
`

const Body: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return (
    <>
      <script dangerouslySetInnerHTML={{ __html: authScript }} />
      <div id="dml-access-gate" role="dialog" aria-modal="true" aria-labelledby="dml-gate-title">
        <div class="dml-gate-card">
          <div class="dml-gate-badge">DML INGENIEROS CONSULTORES</div>
          <h1 id="dml-gate-title">Biblioteca Técnica de Ingeniería de Vapor</h1>
          <p class="dml-gate-subtitle">
            Plataforma de consulta técnica para empleados y clientes autorizados de DML. Ingrese el
            código de acceso corporativo para continuar.
          </p>
          <form id="dml-access-form" autocomplete="off">
            <div class="dml-gate-input-group">
              <input
                id="dml-access-input"
                type="password"
                placeholder="Código de ingreso (ej. DML2026)"
                aria-label="Código de ingreso"
                required
              />
              <button type="submit" class="dml-gate-btn">
                Ingresar al Portal
              </button>
            </div>
            <p id="dml-access-error" class="dml-gate-error" style="display: none;">
              Código de acceso inválido. Verifique con DML Ingenieros Consultores.
            </p>
          </form>
          <div class="dml-gate-footer">
            <span>Acervo Técnico: 131 Manuales · Investigaciones · Data Sheets · Modelos 3D</span>
          </div>
        </div>
      </div>
      <div class="dml-topbar">
        <div class="dml-topbar-inner">
          <div class="dml-topbar-brand">
            <span class="dml-topbar-dot"></span>
            <strong>DML INGENIEROS CONSULTORES</strong>
            <span class="dml-topbar-divider">|</span>
            <span class="dml-topbar-section">División de Ingeniería Térmica y Vapor Industrial</span>
          </div>
          <div class="dml-topbar-actions">
            <span class="dml-topbar-status">Acceso Autorizado</span>
            <button id="dml-logout-btn" type="button" class="dml-logout-btn" title="Bloquear portal">
              🔒 Bloquear
            </button>
          </div>
        </div>
      </div>
      <div id="quartz-body">{children}</div>
    </>
  )
}

export default (() => Body) satisfies QuartzComponentConstructor
