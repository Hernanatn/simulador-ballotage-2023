function actualizarParticipacion()
{
    document.getElementById('salidaParticipacion').innerHTML = document.getElementById('participacion').value;
}
function actualizarMassa()
{
    document.getElementById('salidaMassa').innerHTML = (Math.round(document.getElementById('massaSTM').value*(9645983))).toLocaleString();
}

function actualizarMilei()
{
    document.getElementById('salidaMilei').innerHTML = (Math.round(document.getElementById('mileiJM').value*(7884336))).toLocaleString();
}

function actualizarBullrich()
{
    document.getElementById('salidabullrich').innerHTML = `${(Math.round(document.getElementById('bullrichSTM').value*(6267152))).toLocaleString()} Massa | ${(Math.round((1-document.getElementById('bullrichJM').value)*(6267152))).toLocaleString()} Milei`;
}


function actualizarSchiaretti()
{
    document.getElementById('salidaSchiaretti').innerHTML = `${(Math.round(document.getElementById('schiarettiSTM').value*(1784315))).toLocaleString()} Massa | ${(Math.round((1-document.getElementById('schiarettiJM').value)*(1784315))).toLocaleString()} Milei`;
}

function actualizarBregman() {
    document.getElementById('salidabregman').innerHTML = `${(Math.round(document.getElementById('bregmanSTM').value*(709932))).toLocaleString()} Massa | ${(Math.round((1-document.getElementById('bregmanJM').value)*(709932))).toLocaleString()} Milei`;
}

function actualizarNuevos()
{
    votantesNuevos = ((document.getElementById('participacion').value/100)-(0.775))*34898212;
    if (votantesNuevos < 0)
    {
        document.getElementById('votantesNuevos').textContent = "No fueron a votar";
    }
    else
    {
        document.getElementById('votantesNuevos').textContent = "Nuevos Votantes";
    }

    document.getElementById('salidanuevos').innerHTML = `${(Math.round(document.getElementById('nuevosSTM').value*votantesNuevos)).toLocaleString()} Massa | ${(Math.round((1-document.getElementById('nuevosJM').value)*votantesNuevos)).toLocaleString()} Milei`;
}

function actualizarTodos()
{
    actualizarMassa();
    actualizarMilei();
    actualizarBullrich();
    actualizarSchiaretti();
    actualizarBregman();
    actualizarNuevos();
}

function iniciarPorDefecto()
{
    document.getElementById('participacion').value = 77.5; 
    document.getElementById('massaSTM').value = 0.9; 
    document.getElementById('massaJM').value = 1;
    document.getElementById('mileiJM').value = 0.9; 
    document.getElementById('mileiSTM').value = 1;
    document.getElementById('bullrichSTM').value = 0.4; 
    document.getElementById('bullrichJM').value = 0.6;
    document.getElementById('schiarettiSTM').value = 0.4; 
    document.getElementById('schiarettiJM').value = 0.6;
    document.getElementById('bregmanSTM').value = 0.4; 
    document.getElementById('bregmanJM').value = 0.6;
    document.getElementById('nuevosSTM').value = 0.4; 
    document.getElementById('nuevosJM').value = 0.6; 
}

function devolverValores()
{
    votosValidos    =   Math.round((document.getElementById('participacion').value/100)*34898212);
    votantesNuevos  =   Math.round((document.getElementById('participacion').value/100)*34898212-((0.775)*34898212));

    massaSTM        =   Math.round(document.getElementById('massaSTM').value*(9645983));
    mileiSTM        =   Math.round((1-document.getElementById('mileiSTM').value)*(7884336));
    bullrichSTM     =   Math.round(document.getElementById('bullrichSTM').value*(6267152));
    schiarettiSTM   =   Math.round(document.getElementById('schiarettiSTM').value*(1784315));
    bregmanSTM      =   Math.round(document.getElementById('bregmanSTM').value*(709932));
    nuevosSTM       =   Math.round(document.getElementById('nuevosSTM').value*votantesNuevos);

    massaJM         =   Math.round((1 - document.getElementById('massaJM').value)*(9645983));
    mileiJM         =   Math.round((document.getElementById('mileiJM').value)*(7884336));
    bullrichJM      =   Math.round((1 - document.getElementById('bullrichJM').value)*(6267152));
    schiarettiJM    =   Math.round((1 - document.getElementById('schiarettiJM').value)*(1784315));
    bregmanJM       =   Math.round((1 - document.getElementById('bregmanJM').value)*(709932));
    nuevosJM        =   Math.round((1 - document.getElementById('nuevosJM').value)*votantesNuevos);


    cadenaJSON = `{
        "votosValidos"    : "${votosValidos}",
        "votantesNuevos"  : "${votantesNuevos}",
        "massaSTM"        : "${massaSTM}",
        "mileiSTM"        : "${mileiSTM}",
        "bullrichSTM"     : "${bullrichSTM}",
        "schiarettiSTM"   : "${schiarettiSTM}",
        "bregmanSTM"      : "${bregmanSTM}",
        "nuevosSTM"       : "${nuevosSTM}",
        "massaJM"         : "${massaJM}",
        "mileiJM"         : "${mileiJM}",
        "bullrichJM"      : "${bullrichJM}",        
        "schiarettiJM"    : "${schiarettiJM}",
        "bregmanJM"       : "${bregmanJM}",
        "nuevosJM"        : "${nuevosJM}"}`;

    return JSON.parse(cadenaJSON);
}