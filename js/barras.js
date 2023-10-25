function ajustarBarrasGanador()
{
    let barraSTM = document.getElementById("barraSTM");
    let barraJM = document.getElementById("barraJM");

    let votosAfirmativos = document.getElementById("valores-resultados").getAttribute('votosafirmativos');
    let votosSTM = document.getElementById("valores-resultados").getAttribute('votosstm');
    let votosJM = document.getElementById("valores-resultados").getAttribute('votosjm');
    
    let porcentajeSTM = (votosSTM/votosAfirmativos)*100;
    let porcentajeJM = (votosJM/votosAfirmativos)*100;

    document.getElementById('votos-stm').innerHTML = (votosSTM).toLocaleString();
    document.getElementById('porcentaje-stm').innerHTML = porcentajeSTM.toLocaleString();

    document.getElementById('votos-jm').innerHTML = (votosJM).toLocaleString();
    document.getElementById('porcentaje-jm').innerHTML = porcentajeJM.toLocaleString();
     
    barraSTM.style.width = `${Math.round(porcentajeSTM)}%`;
    barraJM.style.width = `${Math.round(100-porcentajeSTM)}%`;

}