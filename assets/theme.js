/**
 * AMBIKA LIGHTS — LUXURY SHOPIFY THEME ENGINE (theme.js)
 * High performance, zero dependency vanilla JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  initStickyHeader();
  initProductGallery();
  initCCTSelector();
  initPincodeChecker();
  initCartDrawer();
  initAccordions();
  initMobileNav();
  initStickyAddToCart();
});

/* 1. STICKY HEADER SCROLL EFFECT */
function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, { passive: true });
}

/* 2. PRODUCT GALLERY & THUMBNAIL SWITCHER + LIGHT SWITCH */
function initProductGallery() {
  const thumbs = document.querySelectorAll('.pdp-thumb');
  const mainImage = document.querySelector('.pdp-main-image');
  const switchBtns = document.querySelectorAll('[data-light-toggle]');
  const gallery = document.querySelector('.product-hero-gallery');

  if (!mainImage) return;

  // Thumbnail Click Handler
  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      const targetSrc = thumb.dataset.fullSrc || thumb.querySelector('img')?.src;
      if (!targetSrc) return;

      // Smooth image switch with subtle fade
      mainImage.style.opacity = '0.35';
      setTimeout(() => {
        mainImage.src = targetSrc;
        mainImage.style.opacity = '1';
      }, 100);

      // Update active thumbnail border
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');

      // Sync light switch button if index 0 or 1
      const idx = parseInt(thumb.dataset.index, 10);
      if (idx === 0) {
        switchBtns.forEach(b => b.classList.remove('active'));
        document.querySelector('[data-light-toggle="off"]')?.classList.add('active');
        gallery?.classList.remove('light-on-state');
      } else if (idx === 1) {
        switchBtns.forEach(b => b.classList.remove('active'));
        document.querySelector('[data-light-toggle="on"]')?.classList.add('active');
        gallery?.classList.add('light-on-state');
      }
    });
  });

  // Light Switch ON/OFF Controls
  switchBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const mode = btn.getAttribute('data-light-toggle'); // 'on' or 'off'
      switchBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      if (mode === 'on') {
        gallery?.classList.add('light-on-state');
        if (mainImage.dataset.lightOnSrc) {
          mainImage.style.opacity = '0.35';
          setTimeout(() => {
            mainImage.src = mainImage.dataset.lightOnSrc;
            mainImage.style.opacity = '1';
          }, 100);
        }
        // Activate 2nd thumbnail if present
        if (thumbs.length > 1) {
          thumbs.forEach(t => t.classList.remove('active'));
          thumbs[1]?.classList.add('active');
        }
      } else {
        gallery?.classList.remove('light-on-state');
        if (mainImage.dataset.lightOffSrc) {
          mainImage.style.opacity = '0.35';
          setTimeout(() => {
            mainImage.src = mainImage.dataset.lightOffSrc;
            mainImage.style.opacity = '1';
          }, 100);
        }
        // Activate 1st thumbnail
        if (thumbs.length > 0) {
          thumbs.forEach(t => t.classList.remove('active'));
          thumbs[0]?.classList.add('active');
        }
      }
    });
  });
}

/* 3. COLOR TEMPERATURE (CCT) SELECTOR */
function initCCTSelector() {
  const cctCards = document.querySelectorAll('.cct-option-card');
  const selectedCctLabel = document.querySelector('[data-selected-cct]');

  cctCards.forEach(card => {
    card.addEventListener('click', () => {
      cctCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');

      const kelvin = card.dataset.kelvin || '3000K Warm White';
      if (selectedCctLabel) {
        selectedCctLabel.textContent = kelvin;
      }
      
      // Update hidden form input if present
      const hiddenInput = document.querySelector('input[name="properties[Light Temperature]"]');
      if (hiddenInput) {
        hiddenInput.value = kelvin;
      }
    });
  });
}

/* 4. INDIAN PINCODE DELIVERY CHECKER */
function initPincodeChecker() {
  const checkBtn = document.getElementById('pincode-check-btn');
  const input = document.getElementById('pincode-input');
  const resultBox = document.getElementById('pincode-result');

  if (!checkBtn || !input || !resultBox) return;

  const handleCheck = () => {
    const val = input.value.trim();
    if (!/^\d{6}$/.test(val)) {
      resultBox.className = 'pincode-result error';
      resultBox.style.color = '#D9534F';
      resultBox.textContent = 'Please enter a valid 6-digit Indian postal code.';
      resultBox.style.display = 'block';
      return;
    }

    // Pune Pincodes start with 411
    if (val.startsWith('411')) {
      resultBox.className = 'pincode-result success';
      resultBox.style.color = '#B88A52';
      resultBox.innerHTML = `<strong>Pune Delivery Available:</strong> Fast dispatch in 24-48 hrs. Visit our showroom at 354, Budhwar Peth, Near Pasodya Vithoba Temple for live demo & installation setup!`;
    } else {
      resultBox.className = 'pincode-result success';
      resultBox.style.color = '#178B4B';
      resultBox.innerHTML = `<strong>Insured Fragile Shipping:</strong> Delivery in 4-6 business days with wooden crate packing & zero-breakage guarantee.`;
    }
    resultBox.style.display = 'block';
  };

  checkBtn.addEventListener('click', handleCheck);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleCheck();
    }
  });
}

/* 5. SLIDE-OUT CART DRAWER & AJAX HANDLING */
function initCartDrawer() {
  const drawer = document.querySelector('.cart-drawer');
  const overlay = document.querySelector('.cart-drawer-overlay');
  const openTriggers = document.querySelectorAll('[data-open-cart]');
  const closeTriggers = document.querySelectorAll('[data-close-cart]');
  const itemsContainer = document.getElementById('cart-drawer-items');
  const footerContainer = document.getElementById('cart-drawer-footer');

  if (!drawer || !overlay) return;

  const formatMoney = (cents) => {
    return '₹' + Math.round(Number(cents) / 100).toLocaleString('en-IN');
  };

  const renderCartDrawer = (cart) => {
    // 1. Update all cart count badges across the page
    document.querySelectorAll('.cart-count-badge').forEach(badge => {
      badge.textContent = cart.item_count || 0;
    });

    // 2. Empty state handling
    if (!cart.items || cart.items.length === 0) {
      if (itemsContainer) {
        itemsContainer.innerHTML = `
          <div class="cart-empty-state" style="text-align: center; padding: 60px 20px;">
            <p style="color: var(--color-muted); margin-bottom: 24px; font-size: 14.5px;">Your luxury shopping bag is empty.</p>
            <a href="/collections/all" class="btn btn-outline-gold" data-close-cart style="padding: 10px 24px; font-size: 11px;">Explore Catalogue</a>
          </div>
        `;
        const emptyCloseBtn = itemsContainer.querySelector('[data-close-cart]');
        if (emptyCloseBtn) emptyCloseBtn.addEventListener('click', closeDrawer);
      }
      if (footerContainer) {
        footerContainer.style.display = 'none';
      }
      return;
    }

    // 3. Render active cart items
    if (footerContainer) {
      footerContainer.style.display = 'block';
      const subtotalEl = footerContainer.querySelector('.cart-drawer-subtotal');
      if (subtotalEl) {
        subtotalEl.textContent = formatMoney(cart.total_price);
      }
    }

    if (itemsContainer) {
      itemsContainer.innerHTML = cart.items.map(item => {
        const itemImg = item.image || item.featured_image ? (item.image || item.featured_image.url) : '';
        const itemTitle = item.product_title || item.title;
        const itemSku = item.sku ? `<div style="font-size: 11px; color: var(--color-primary-hover); font-weight: 600; margin-bottom: 4px;">SKU: ${item.sku}</div>` : '';
        const variantTitle = (item.variant_title && item.variant_title !== 'Default Title') 
          ? `<div style="font-size: 11.5px; color: var(--color-muted); margin-bottom: 6px;">${item.variant_title}</div>` 
          : '';

        return `
          <div class="cart-item" data-item-key="${item.key}" style="display: flex; gap: 16px; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid var(--color-border); align-items: flex-start;">
            <a href="${item.url}" style="flex-shrink: 0; width: 75px; height: 90px; overflow: hidden; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: #F3EFE6; display: flex; align-items: center; justify-content: center;">
              ${itemImg ? `<img src="${itemImg}" alt="${itemTitle}" width="75" height="90" style="width: 100%; height: 100%; object-fit: cover;">` : `<div style="color: #999; font-size: 10px;">Illume & Co</div>`}
            </a>
            <div style="flex-grow: 1; min-width: 0;">
              <h4 style="font-size: 15px; margin: 0 0 4px; font-family: var(--font-serif); line-height: 1.3;">
                <a href="${item.url}" style="text-decoration: none; color: var(--color-ink);">${itemTitle}</a>
              </h4>
              ${itemSku}
              ${variantTitle}
              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <div class="cart-qty-selector" style="display: inline-flex; align-items: center; border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: #FFF;">
                  <button type="button" class="cart-qty-btn" data-change="-1" data-key="${item.key}" data-qty="${item.quantity}" style="background: none; border: none; padding: 4px 10px; cursor: pointer; font-size: 14px; color: var(--color-ink);" aria-label="Decrease quantity">−</button>
                  <span style="font-size: 12px; font-weight: 600; padding: 0 6px; min-width: 20px; text-align: center;">${item.quantity}</span>
                  <button type="button" class="cart-qty-btn" data-change="1" data-key="${item.key}" data-qty="${item.quantity}" style="background: none; border: none; padding: 4px 10px; cursor: pointer; font-size: 14px; color: var(--color-ink);" aria-label="Increase quantity">+</button>
                </div>
                <div style="font-weight: 600; font-size: 13.5px; color: var(--color-ink);">${formatMoney(item.line_price)}</div>
              </div>
            </div>
            <button type="button" class="cart-item-remove" data-key="${item.key}" title="Remove item" aria-label="Remove ${itemTitle}" style="background: none; border: none; color: var(--color-muted); cursor: pointer; font-size: 20px; line-height: 1; padding: 0 4px; margin-left: 4px;">&times;</button>
          </div>
        `;
      }).join('');

      // Attach quantity adjustment buttons
      itemsContainer.querySelectorAll('.cart-qty-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.preventDefault();
          const key = btn.dataset.key;
          const currentQty = parseInt(btn.dataset.qty, 10);
          const change = parseInt(btn.dataset.change, 10);
          const newQty = Math.max(0, currentQty + change);
          await updateLineItem(key, newQty);
        });
      });

      // Attach remove item buttons
      itemsContainer.querySelectorAll('.cart-item-remove').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.preventDefault();
          const key = btn.dataset.key;
          await updateLineItem(key, 0);
        });
      });
    }
  };

  const updateLineItem = async (key, quantity) => {
    try {
      if (itemsContainer) itemsContainer.style.opacity = '0.5';
      const res = await fetch('/cart/change.js', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ id: key, quantity: quantity })
      });
      if (res.ok) {
        const updatedCart = await res.json();
        renderCartDrawer(updatedCart);
      }
    } catch (err) {
      console.error('Error changing cart item:', err);
    } finally {
      if (itemsContainer) itemsContainer.style.opacity = '1';
    }
  };

  const fetchAndRenderCart = async () => {
    try {
      const res = await fetch('/cart.js', { headers: { 'Accept': 'application/json' } });
      if (res.ok) {
        const cart = await res.json();
        renderCartDrawer(cart);
      }
    } catch (err) {
      console.error('Error fetching cart data:', err);
    }
  };

  const openDrawer = async () => {
    drawer.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    await fetchAndRenderCart();
  };

  const closeDrawer = () => {
    drawer.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  };

  openTriggers.forEach(btn => btn.addEventListener('click', (e) => {
    e.preventDefault();
    openDrawer();
  }));

  closeTriggers.forEach(btn => btn.addEventListener('click', closeDrawer));
  overlay.addEventListener('click', closeDrawer);

  // Intercept Shopify Add to Cart forms for AJAX drawer experience
  document.querySelectorAll('form[action*="/cart/add"]').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('[type="submit"]');
      const origText = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Adding to Bag...';
      }

      try {
        const formData = new FormData(form);
        const res = await fetch('/cart/add.js', {
          method: 'POST',
          body: formData,
          headers: { 'Accept': 'application/json' }
        });

        if (res.ok) {
          await openDrawer();
        } else {
          form.submit(); // fallback to standard submit if shopify error
        }
      } catch (err) {
        console.error('Cart add error:', err);
        form.submit();
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = origText;
        }
      }
    });
  });

  // Preload cart count and items on page initialization
  fetchAndRenderCart();
}

async function updateCartBadge() {
  try {
    const res = await fetch('/cart.js', { headers: { 'Accept': 'application/json' } });
    if (res.ok) {
      const cart = await res.json();
      document.querySelectorAll('.cart-count-badge').forEach(badge => {
        badge.textContent = cart.item_count || 0;
      });
    }
  } catch (err) {
    console.error('Error updating cart count:', err);
  }
}

/* 6. COLLAPSIBLE ACCORDIONS (PDP SPECS & FAQ) */
function initAccordions() {
  const triggers = document.querySelectorAll('.accordion-trigger');
  triggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const panel = trigger.nextElementSibling;
      const isOpen = trigger.classList.contains('active');

      if (isOpen) {
        trigger.classList.remove('active');
        if (panel) panel.style.display = 'none';
      } else {
        trigger.classList.add('active');
        if (panel) panel.style.display = 'block';
      }
    });
  });
}

/* 7. MOBILE NAVIGATION */
function initMobileNav() {
  const toggleBtn = document.querySelector('[data-mobile-menu-toggle]');
  const mobileNav = document.querySelector('.mobile-nav-drawer');
  const overlay = document.querySelector('.mobile-nav-overlay');
  const closeBtns = document.querySelectorAll('[data-mobile-menu-close]');
  const accordions = document.querySelectorAll('.mobile-accordion-toggle');

  if (!mobileNav) return;

  const openNav = () => {
    mobileNav.classList.add('active');
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closeNav = () => {
    mobileNav.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (toggleBtn) {
    toggleBtn.addEventListener('click', openNav);
  }

  closeBtns.forEach(btn => {
    btn.addEventListener('click', closeNav);
  });

  if (overlay) {
    overlay.addEventListener('click', closeNav);
  }

  accordions.forEach(acc => {
    acc.addEventListener('click', () => {
      const parent = acc.closest('.mobile-nav-accordion');
      if (parent) {
        parent.classList.toggle('active');
      }
    });
  });
}

/* 8. STICKY ADD TO CART BAR ON SCROLL */
function initStickyAddToCart() {
  const stickyBar = document.querySelector('.sticky-pdp-bar');
  const mainBuyBtn = document.querySelector('.pdp-buy-button');

  if (!stickyBar || !mainBuyBtn) return;

  const observer = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) {
      stickyBar.classList.add('visible');
    } else {
      stickyBar.classList.remove('visible');
    }
  }, { threshold: 0 });

  observer.observe(mainBuyBtn);
}
