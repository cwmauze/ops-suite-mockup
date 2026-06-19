var window = { FAA_AIRPORTS: [] };
var document = {
    readyState: 'complete',
    createElement: function() { return { style: {}, appendChild: function(){}, setAttribute: function(){} }; },
    head: { appendChild: function(){} },
    body: { appendChild: function(){} },
    getElementById: function() { return { addEventListener: function(){}, style: {} }; },
    addEventListener: function(e, cb){ if(e==='DOMContentLoaded') cb(); }
};
var localStorage = { getItem: function(){ return null; }, setItem: function(){} };
