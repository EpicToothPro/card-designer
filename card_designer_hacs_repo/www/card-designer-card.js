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
    const template = this._config.template || '';
    const context = this._config.context || {};

    const container = document.createElement('div');
    container.innerHTML = `<div class="card"><ha-card><div class="card-content">Loading...</div></ha-card></div>`;
    this.shadowRoot.innerHTML = '';
    this.shadowRoot.appendChild(container);

    try {
      const resp = await fetch('/api/card_designer/render', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({template: template, context: context})
      });
      const data = await resp.json();
      if (data && data.result !== undefined) {
        this.shadowRoot.querySelector('.card-content').innerHTML = data.result;
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

  getCardSize() {
    return 3;
  }
}

customElements.define('card-designer-card', CardDesignerCard);
