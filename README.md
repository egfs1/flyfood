  # **Universidade Federal Rural de Pernambuco**

   # **Departamento de Estatística e Informática**

   Bacharelado em Sistemas de Informação

   DOCUMENTO COMPLETO EM :
   
   https://docs.google.com/document/d/1B4rA023PbQ5A0nl9cFrVZTkHCOIbqvylQeYyecw9KS8/edit?tab=t.0#heading=h.gjdgxs
		

# **F L Y F O O D**


**Autores:**  
Eduardo Souza - eduardo.gomesferreira@ufrpe.br  
Rodrigo Santana - rodrigo.sousasantana@ufrpe.br  
Victor Souza - victor.souzaa@ufrpe.br  
Roberto Leite - roberto.opleite@ufrpe.br  
Matheus Sales - matheus.costasales@ufrpe.br  


**Orientador:**  
Rodrigo Gabriel Ferreira Soares


**Recife**
Março de 2025


# **Resumo** 

   Com o grande crescimento do comércio on-line e a popularização de serviços de entrega, a logística urbana enfrenta grandes dificuldades, especialmente em cenários de congestionamento de trânsito. Empresas de entregas buscam alternativas inovadoras para atender à alta demanda, reduzindo custos e melhorando a eficiência dos serviços prestados. Drones de entregas surgem como uma alternativa promissora, mas encaram limitações como a autonomia de baterias, tornando crucial a otimização das rotas. O objetivo deste projeto foi desenvolver algoritmos que determinam a rota mais curta possível para drones de entrega, a fim de maximizar a eficiência operacional, minimizando o consumo de energia dos drones.  
   Inicialmente, o algoritmo foi desenvolvido utilizando a abordagem de força bruta, resolvendo o problema do caixeiro viajante TSP. Esta abordagem avalia todas as possíveis permutações das rotas para garantir o melhor trajeto viável. No entanto, devido à sua complexidade computacional fatorial (O(n!)), a força bruta se mostrou impraticável para grandes quantidades de pontos de entrega. Para superar essa limitação, foram implementadas três heurísticas: a heurística 2-opt, que realiza trocas locais para melhorar rotas existentes; o algoritmo genético, que simula a evolução de soluções por meio de seleção, cruzamento e mutação; e a colônia de formigas, que utiliza comportamento coletivo para explorar caminhos promissores.  
   A solução algorítmica foi testada em cenários simulados, com pequenos e médios conjuntos de pontos de entregas. A força bruta demonstrou eficácia na determinação da rota mais curta para instâncias pequenas, enquanto as heurísticas apresentaram resultados satisfatórios em cenários maiores, com complexidade reduzida para polinomial O(n²). Os resultados confirmam a viabilidade de usar força bruta para a validação de soluções ótimas em pequena escala, enquanto as heurísticas se mostraram adequadas para aplicações práticas em larga escala.  
   Portanto, embora a abordagem por força bruta seja computacionalmente intensiva, ela fornece uma base confiável para avaliar outras técnicas de otimização, como as heurísticas. O desenvolvimento deste projeto reforça a importância de integrar a ciência da computação e tecnologias emergentes para enfrentar desafios logísticos da atualidade, destacando o potencial das heurísticas como ferramentas eficientes para a otimização de rotas de drones.
