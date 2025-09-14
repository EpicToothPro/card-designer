class CardDesignerCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({mode: 'open'});
    this._config = {};
  }

  setConfig(config) {
    this._config = config || {};
    this.render();
  }

  async render() {
    const title = this._config.title || '';
    const template = this._config.template || '';
    const context = this._config.context || {};

    // Create basic container
    const container = document.createElement('div');
    container.innerHTML = `<div class="card"><ha-card><div class="card-content">Loading...</div></ha-card></div>`;
    // Clear previous
    this.shadowRoot.innerHTML = '';
    this.shadowRoot.appendChild(container);

    // Try to render server-side
    try {
      const resp = await fetch('/api/card_designer/render', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({template: template, context: context})
      });
      const data = await resp.json();
      if (data && data.result !== undefined) {
        const content = this.shadowRoot.querySelector('.card-content');
        content.innerHTML = data.result;
      } else {
        this._showError('no_result');
      }
    } catch (e) {
      this._showError(e);
    }
  }

  _showError(err) {
    this.shadowRoot.innerHTML = `<div class="card"><ha-card><div class="card-content">Error: ${err}</div></ha-card></div>`;
  }

  // Define card size for Lovelace
  getCardSize() {
    return 3;
  }
}

customElements.define('card-designer-card', CardDesignerCard);
