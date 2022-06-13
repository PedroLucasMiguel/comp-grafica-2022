'''
\begin{table}[]
\centering
\begin{tabular}{|c|c|c|}
\hline
\textbf{Imagem}          & \textbf{Raiz do erro médio quadrático} & \textbf{Coeficiente de Jaccard} \\ \hline
C (Sal e Pimenta) y=0,4  & 73.77031146165383                      & 0.005340576171875               \\ \hline
C (Sal e Pimenta) y=0,04 & 177.66986324924898                     & 0.014801025390625               \\ \hline
C (Uniforme) y=0,4       & 80.64413059585023                      & 0.006561279296875               \\ \hline
C (Uniforme) y=0,04      & 178.83060632186618                     & 0.012969970703125               \\ \hline
C (Gaussiano) y=0,4      & 85.79021798594054                      & 0.13824462890625                \\ \hline
C (Gaussiano) y=0,04     & 176.79153636334493                     & 0.0110321044921875              \\ \hline
\end{tabular}
\end{table}
'''

def parse(txt):

    f_in_lines = []

    with open('output.txt', 'r') as f:
        f_in_lines = f.readlines()

    with open('text-stuff.txt', 'w') as f:
        metrics = f_in_lines[0].split(' | ')
        rows = len(metrics)



if __name__ == '__main__':
    pass