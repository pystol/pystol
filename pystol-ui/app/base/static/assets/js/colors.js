/* global rgbToHex */

/**
 * --------------------------------------------------------------------------
 * CoreUI Free Boostrap Admin Template (v3.0.0-alpha.1): colors.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */
document.querySelectorAll('.theme-color').forEach(function (element) {
  var color = getComputedStyle(element, null).getPropertyValue('background-color');
  var table = document.createElement('table');
  table.classList.add('w-100');
  table.innerHTML = "\n      <table class=\"w-100\">\n        <tr>\n          <td class=\"text-muted\">HEX:</td>\n          <td class=\"font-weight-bold\">" + rgbToHex(color) + "</td>\n        </tr>\n        <tr>\n          <td class=\"text-muted\">RGB:</td>\n          <td class=\"font-weight-bold\">" + color + "</td>\n        </tr>\n      </table>\n    ";
  element.parentNode.appendChild(table);
});
//# sourceMappingURL=colors.js.map