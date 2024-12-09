document$.subscribe(function () {
  if (
    (window.location.hostname === 'scs.owasp.org' || window.location.hostname === 'localhost') &&
    (window.location.pathname.startsWith('/SCSTG') || window.location.pathname.startsWith('/SCSVS'))
  ) {
    const links = document.links;

    for (let i = 0; i < links.length; i++) {
      const link = links[i];

      // Exclude links to scs.owasp.org
      if (link.hostname === 'scs.owasp.org') {
        continue; // Skip this link
      }

      // Exclude links that include github.com/OWASP
      if (link.href.includes('github.com/OWASP')) {
        continue; // Skip this link
      }

      if (link.hostname !== window.location.hostname) {
        link.setAttribute('target', '_blank');

        // Create an icon element (e.g., a small arrow)
        const icon = document.createElement('span');
        icon.textContent = ' ↗';

        // Append the icon to the link
        link.appendChild(icon);
      }
    }
  }
})
