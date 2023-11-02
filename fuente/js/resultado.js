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

function ajustarBarrasGanador()
{
    console.log("# [DEBUG] <ajustarBarrasGanador()>")
    let barraSTM = document.getElementById("barraSTM");
    let barraJM = document.getElementById("barraJM");

    let votosAfirmativos = document.getElementById("valores-resultados").getAttribute('votosafirmativos');
    let votosSTM = document.getElementById("valores-resultados").getAttribute('votosstm');
    let votosJM = document.getElementById("valores-resultados").getAttribute('votosjm');
    
console.log(`# [DEBUG]\tVotos\t\t\t|\n\t\t\t${votosAfirmativos}\t\t|\n\t\t\t${votosSTM} STM\t|\n\t\t\t${votosJM} JM\t|\n`) 

    let porcentajeSTM = (votosSTM/votosAfirmativos)*100;
    let porcentajeJM = (votosJM/votosAfirmativos)*100;

    document.getElementById('votos-stm').innerHTML = (votosSTM).toLocaleString();
    document.getElementById('porcentaje-stm').innerHTML = porcentajeSTM.toLocaleString();

    document.getElementById('votos-jm').innerHTML = (votosJM).toLocaleString();
    document.getElementById('porcentaje-jm').innerHTML = porcentajeJM.toLocaleString();
    console.log(`# [DEBUG] ${Math.round(porcentajeSTM)}% STM | ${Math.round(100 - porcentajeSTM)}% JM |`) 
    barraSTM.style.width = `${Math.round(porcentajeSTM)}%`;
    barraJM.style.width = `${Math.round(100-porcentajeSTM)}%`;
    console.log("# [DEBUG] </ajustarBarrasGanador>")
}

function actualizarVotos()
{
    console.log("# [DEBUG] <actualizarVotos()>");
    let votantesNuevos  =   Math.round((document.getElementById('participacion').value/100)*34898212-((0.775)*34898212));
    
    let massaSTM        =   Math.round(document.getElementById('massaSTM').value*(9645983));
    let mileiSTM        =   Math.round((1-document.getElementById('mileiSTM').value)*(7884336));
    let bullrichSTM     =   Math.round(document.getElementById('bullrichSTM').value*(6267152));
    let schiarettiSTM   =   Math.round(document.getElementById('schiarettiSTM').value*(1784315));
    let bregmanSTM      =   Math.round(document.getElementById('bregmanSTM').value*(709932));
    let nuevosSTM       =   Math.round(document.getElementById('nuevosSTM').value*votantesNuevos);
    
    let massaJM         =   Math.round((1 - document.getElementById('massaJM').value)*(9645983));
    let mileiJM         =   Math.round((document.getElementById('mileiJM').value)*(7884336));
    let bullrichJM      =   Math.round((1 - document.getElementById('bullrichJM').value)*(6267152));
    let schiarettiJM    =   Math.round((1 - document.getElementById('schiarettiJM').value)*(1784315));
    let bregmanJM       =   Math.round((1 - document.getElementById('bregmanJM').value)*(709932));
    let nuevosJM        =   Math.round((1 - document.getElementById('nuevosJM').value)*votantesNuevos);
    
    var totalesSTM    = massaSTM+mileiSTM+bullrichSTM+schiarettiSTM+bregmanSTM+nuevosSTM;
    var totalesJM    = massaJM+mileiJM+bullrichJM+schiarettiJM+bregmanJM+nuevosJM;
    var afirmativos = totalesJM + totalesSTM

    document.getElementById("valores-resultados").setAttribute('votosafirmativos',afirmativos);
    document.getElementById("valores-resultados").setAttribute('votosstm',totalesSTM);
    document.getElementById("valores-resultados").setAttribute('votosjm',totalesJM);
    document.getElementById('porcentaje-stm').innerHTML = totalesSTM/afirmativos.toLocaleString();
    document.getElementById('porcentaje-jm').innerHTML = totalesJM/afirmativos.toLocaleString();
    console.log(`# [DEBUG] Totales STM: ${totalesSTM} | TotalesJM : ${totalesJM}`);
    console.log("# [DEBUG] </actualizarVotos()>");
}


