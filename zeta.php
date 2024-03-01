<?php
// Conecte ao banco de dados local
$conexao = new mysqli('localhost', 'seu_usuario', 'sua_senha', 'seu_banco_de_dados');

if ($conexao->connect_error) {
    die("Erro na conexão: " . $conexao->connect_error);
}

// Obtenha os dados do arquivo com base no ID
$id = $_GET['id'];
$consulta = $conexao->query("SELECT nome_do_arquivo, dados_do_arquivo FROM Arquivos WHERE id = $id");

if ($consulta->num_rows > 0) {
    $dados_do_arquivo = $consulta->fetch_assoc();

    // Emita os cabeçalhos apropriados
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="' . $dados_do_arquivo['nome_do_arquivo'] . '"');

    // Saída dos dados do arquivo
    echo $dados_do_arquivo['dados_do_arquivo'];
} else {
    echo "Arquivo não encontrado.";
}

// Feche a conexão com o banco de dados
$conexao->close();
?>
