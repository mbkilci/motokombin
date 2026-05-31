import { useState } from 'react';

function App() {
  const [tabs, setTabs] = useState([{ id: 1, name: 'Şehir Kombini', gear: { kask: null, mont: null, eldiven: null, pantolon: null, bot: null } }]);
  const [activeTabId, setActiveTabId] = useState(1);
  const activeTab = tabs.find(t => t.id === activeTabId) || tabs[0];
  const gear = activeTab.gear;

  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [linkInput, setLinkInput] = useState('');
  const [loadingSlots, setLoadingSlots] = useState({}); 

  const extractPrice = (priceStr) => {
    if (!priceStr || priceStr.includes("Bulunamadı")) return 0;
    return parseFloat(priceStr.replace(/\./g, '').replace(',', '.').replace(/[^0-9.]/g, '')) || 0;
  };
  const totalPrice = Object.values(gear).reduce((sum, item) => sum + (item ? extractPrice(item.price) : 0), 0);

  const openDrawer = (slotType) => {
    setSelectedSlot(slotType);
    setLinkInput('');
    setIsDrawerOpen(true);
  };

  const removeGear = (type, e) => {
    e.preventDefault(); e.stopPropagation();
    setTabs(currentTabs => currentTabs.map(tab => tab.id === activeTabId ? { ...tab, gear: { ...tab.gear, [type]: null } } : tab));
  };

  const handleProcessGear = async () => {
    if (!linkInput) return;
    const targetSlot = selectedSlot;
    const currentTabId = activeTabId;
    const targetLink = linkInput;

    setIsDrawerOpen(false); // Çekmeceyi anında kapat
    setLoadingSlots(prev => ({ ...prev, [targetSlot]: true })); // Ana ekranda loading göster

    try {
      // Doğrudan ana API'ye gidiyoruz (Eski hızlı sürüm)
      const response = await fetch('http://127.0.0.1:8000/api/process-gear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: targetLink, type: targetSlot })
      });
      
      const data = await response.json();
      
      if (data.success) {
        const timestampedUrl = `${data.image_url}?t=${Date.now()}`;
        setTabs(currentTabs => currentTabs.map(tab => 
          tab.id === currentTabId ? { ...tab, gear: { ...tab.gear, [targetSlot]: { url: timestampedUrl, price: data.price, originalUrl: targetLink } } } : tab
        ));
      } else {
        alert("Görsel işlenemedi.");
      }
    } catch (error) {
      alert("Sunucuya bağlanılamadı.");
    } finally {
      setLoadingSlots(prev => ({ ...prev, [targetSlot]: false }));
    }
  };

  const Zone = ({ type, label, top, left, width, height }) => {
    const hasItem = gear[type] !== null;
    const isLoading = loadingSlots[type];

    return (
      <div 
        onClick={() => openDrawer(type)}
        className={`absolute cursor-pointer flex flex-col items-center justify-center transition-all duration-300 group z-20
          ${!hasItem ? 'border-2 border-dashed border-zinc-700 hover:border-orange-500 bg-zinc-900/30 hover:bg-zinc-800/80 rounded-2xl backdrop-blur-sm' : ''}
          ${hasItem ? 'hover:bg-white/10 rounded-2xl' : ''} 
        `}
        style={{ top, left, width, height }}
      >
        {isLoading && (
          <div className="bg-zinc-900/80 px-3 py-1 rounded-full border border-orange-500/50 backdrop-blur-md">
             <span className="animate-pulse text-orange-400 font-bold text-[10px] tracking-wider">İŞLENİYOR</span>
          </div>
        )}
        {!hasItem && !isLoading && (
          <div className="flex flex-col items-center justify-center text-zinc-500 group-hover:text-orange-400 transition-colors">
            <span className="text-xs font-bold uppercase tracking-widest text-center">{label}</span>
            <span className="opacity-0 group-hover:opacity-100 bg-orange-500 text-white rounded-full w-6 h-6 flex items-center justify-center font-bold shadow-lg mt-1 transition-opacity">+</span>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-zinc-950 p-4 md:p-8 flex flex-col max-w-7xl mx-auto text-white overflow-x-hidden">
      
      <header className="mb-6 md:mb-10 w-full border-b border-zinc-800 pb-2">
        <h1 className="text-2xl md:text-3xl font-black mb-4">MOTO<span className="text-orange-500">KOMBIN</span></h1>
      </header>

      <div className="flex flex-col lg:flex-row gap-8 lg:gap-12 flex-1 items-center lg:items-start">
        
        {/* ANA KOMBİN ALANI */}
        <div className="relative w-[400px] h-[700px] transform scale-[0.85] md:scale-100 origin-top shrink-0">
          {Object.entries(gear).map(([type, item]) => {
            if (item && !loadingSlots[type]) {
              return <img key={type} src={item.url} alt={type} className="absolute inset-0 w-full h-full object-contain pointer-events-none z-10 drop-shadow-2xl transition-opacity duration-500" />
            }
            return null;
          })}

          {/* Eldiven ve Bot zone'ları biraz büyütüldü */}
          <Zone type="kask" label="Kask" top="4%" left="32%" width="36%" height="18%" />
          <Zone type="mont" label="Mont" top="24%" left="25%" width="50%" height="28%" />
          <Zone type="eldiven" label="Eldiven" top="54%" left="12%" width="18%" height="18%" />
          <Zone type="eldiven" label="Eldiven" top="54%" left="70%" width="18%" height="18%" />
          <Zone type="pantolon" label="Pantolon" top="54%" left="35%" width="30%" height="32%" />
          <Zone type="bot" label="Bot" top="86%" left="30%" width="18%" height="14%" />
          <Zone type="bot" label="Bot" top="86%" left="52%" width="18%" height="14%" />
        </div>

        {/* HESAP ÖZETİ */}
        <div className="w-full lg:w-80 bg-zinc-900 rounded-3xl p-6 md:p-8 border border-zinc-800 h-fit shadow-xl mb-10 lg:mb-0">
          <h2 className="text-xl font-bold mb-6 border-b border-zinc-800 pb-4 text-white">Özet</h2>
          <div className="space-y-2 mb-8">
            {[ { label: 'Kask', key: 'kask' }, { label: 'Mont', key: 'mont' }, { label: 'Eldiven', key: 'eldiven' }, { label: 'Pantolon', key: 'pantolon' }, { label: 'Bot', key: 'bot' } ].map(item => {
              const gearItem = gear[item.key];
              const isAdded = !!gearItem;
              return (
                <div key={item.key} className={`flex justify-between items-center text-sm p-3 -mx-3 rounded-xl transition-all ${isAdded ? 'hover:bg-zinc-800 group' : ''}`}>
                  <a href={isAdded ? gearItem.originalUrl : undefined} target="_blank" rel="noreferrer" className={`flex-1 flex items-center gap-2 ${isAdded ? 'cursor-pointer text-orange-400 group-hover:text-orange-300 font-medium' : 'cursor-default text-zinc-500'}`}>
                    {item.label}
                  </a>
                  <div className="flex items-center">
                    <span className={`font-mono ${isAdded ? "text-zinc-200" : "text-zinc-700"}`}>{gearItem?.price || '-'}</span>
                    {isAdded && <button onClick={(e) => removeGear(item.key, e)} className="ml-3 text-zinc-600 hover:text-red-500">✕</button>}
                  </div>
                </div>
              )
            })}
          </div>
          <div className="border-t border-zinc-800 pt-6">
            <span className="text-zinc-400 text-sm block mb-1 font-medium">Toplam Tutar</span>
            <span className="text-3xl font-black text-orange-500 tracking-tight">{totalPrice.toLocaleString('tr-TR')} TL</span>
          </div>
        </div>
      </div>

      {isDrawerOpen && (
        <>
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40" onClick={() => setIsDrawerOpen(false)} />
          <div className="fixed right-0 top-0 h-full w-[100vw] sm:w-[500px] bg-zinc-950 border-l border-zinc-800 z-50 p-6 md:p-8 flex flex-col shadow-2xl">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-2xl font-black text-white capitalize">{selectedSlot} Ekle</h2>
              <button onClick={() => setIsDrawerOpen(false)} className="text-2xl text-zinc-500 hover:text-white">&times;</button>
            </div>
            
            <input type="text" value={linkInput} onChange={(e) => setLinkInput(e.target.value)} placeholder="Ürün linkini yapıştırın..." className="w-full bg-zinc-900 border-2 border-zinc-800 rounded-2xl p-4 text-white focus:border-orange-500 outline-none mb-6 font-mono text-sm" />
            <button onClick={handleProcessGear} disabled={!linkInput} className={`w-full py-4 rounded-2xl font-black text-lg ${!linkInput ? 'bg-zinc-800 text-zinc-600' : 'bg-orange-500 text-white hover:bg-orange-400 shadow-[0_0_20px_rgba(249,115,22,0.2)]'}`}>
              Kombine Ekle
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default App;