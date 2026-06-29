---
title: "Semi-Supervised Classification with Graph Convolutional Networks"
authors: [Thomas N. Kipf, Max Welling]
year: 2017
source: "ICLR 2017 conference paper; arXiv:1609.02907v4 [cs.LG], 22 Feb 2017"
tags: [paper-card, study, graph-neural-network, gcn]
---

# Semi-Supervised Classification with Graph Convolutional Networks

## 30초 요약

이 논문은 그래프에서 일부 노드에만 라벨이 있을 때, 라벨이 없는 노드까지 함께 활용해 노드를 분류하는 Graph Convolutional Network(GCN)를 제안한다. 핵심은 각 노드가 자기 feature만 보는 것이 아니라, 연결된 이웃 노드의 feature를 정규화해서 섞으며 표현을 업데이트하는 것이다. 저자들은 이 단순한 propagation rule이 citation network와 NELL 지식 그래프에서 당시 주요 baseline보다 좋은 정확도를 낸다고 보고한다.

## 이 논문이 풀려는 문제

많은 실제 데이터는 표나 이미지처럼 독립된 샘플 묶음이 아니라 그래프다. 논문 인용망에서는 문서가 노드이고 인용 관계가 edge다. 문제는 모든 문서에 라벨이 붙어 있지 않고, 보통 일부 문서에만 주제가 알려져 있다는 점이다.

기존 방식은 연결된 노드는 비슷한 라벨을 가질 것이라는 가정을 loss에 직접 넣는 경우가 많았다. 이 논문은 그 대신 그래프 구조 자체를 신경망의 입력으로 넣어, 노드 feature와 이웃 관계를 함께 학습한다.

## 핵심 아이디어 3개

- 그래프를 정규화 항으로만 쓰지 않고, 모델을 `f(X, A)`로 만들어 node feature `X`와 adjacency matrix `A`를 함께 사용한다.
- 각 layer에서 노드는 자기 자신과 이웃 노드의 표현을 정규화해서 섞고, 그 결과에 trainable weight를 곱한다.
- 라벨이 있는 노드에 대해서만 loss를 계산하지만, adjacency를 통해 라벨 없는 노드의 표현도 함께 갱신된다.

## 그림으로 이해하기

Figure 1은 GCN의 직관을 보여준다. 같은 graph edge가 여러 layer에서 공유되고, 각 노드는 이웃과 정보를 주고받으며 hidden representation을 만든다. 오른쪽 t-SNE 그림은 Cora 데이터에서 5% 라벨만 사용해도 hidden representation이 class별로 어느 정도 분리되는 모습을 보여준다.

Table 2는 결과표를 읽는 법을 보여주기 좋다. 행은 비교 방법, 열은 데이터셋, 숫자는 정확도다. GCN은 Citeseer 70.3%, Cora 81.5%, Pubmed 79.0%, NELL 66.0%를 기록해 표에 있는 Planetoid 결과보다 모두 높게 보고된다. 이 결과는 특정 transductive benchmark에서의 결과이며, 모든 그래프 문제에서 항상 GCN이 최고라는 뜻은 아니다.

## 꼭 기억할 수식

먼저 용어 5개:
- node: 그래프의 점
- edge: 점과 점 사이의 연결
- feature: 각 node가 가진 정보
- adjacency matrix: 어떤 node들이 연결되어 있는지 적은 표
- self-loop: 자기 자신도 참고하게 하는 연결

GCN layer의 핵심은 정규화된 adjacency로 이웃 정보를 섞는 것이다.

$$
H^{(l+1)} =
\sigma\left(
\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}H^{(l)}W^{(l)}
\right)
$$

여기서 `\tilde{A} = A + I`는 self-loop를 추가한 adjacency matrix이고, `\tilde{D}`는 그 degree matrix다. 그냥 이웃 정보를 더하기만 하면 친구가 많은 노드의 값이 너무 커질 수 있으므로, 연결 수를 반영해 균형을 맞춘다고 보면 된다.

두 층 node classification 모델은 다음처럼 쓸 수 있다.

$$
Z =
\mathrm{softmax}
\left(
\hat{A}\,\mathrm{ReLU}\left(\hat{A}XW^{(0)}\right)W^{(1)}
\right)
$$

## 예시로 이해하기

Cora citation network를 생각해보자. 노드는 논문이고, edge는 논문 사이의 인용 관계다. 어떤 논문에는 "Neural Networks", "Probabilistic Methods" 같은 class label이 있지만 대부분의 논문에는 label이 없다고 하자.

GCN은 각 논문의 bag-of-words feature만 보는 것이 아니라, 그 논문이 인용하거나 인용받은 이웃 논문의 feature도 함께 섞는다. 첫 번째 layer에서는 가까운 이웃의 정보가 들어오고, 두 번째 layer에서는 이웃의 이웃 정보까지 간접적으로 반영된다. 그래서 라벨이 적어도 graph structure가 의미 있는 경우에는 더 좋은 node representation을 만들 수 있다.

## 이 논문을 읽고 나면 알게 되는 것

- GCN의 기본 propagation rule이 무엇인지 설명할 수 있다.
- 왜 self-loop와 symmetric normalization이 중요한지 이해할 수 있다.
- semi-supervised node classification에서 라벨 없는 노드가 어떻게 학습에 간접적으로 기여하는지 이해할 수 있다.
- GCN이 이후 GraphSAGE, GAT, message passing GNN을 읽기 위한 기준점이라는 것을 알 수 있다.

## 다음에 읽으면 좋은 것

- Chebyshev graph convolution: Defferrard et al., "Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering"
- Inductive GNN: GraphSAGE
- Attention 기반 GNN: Graph Attention Networks(GAT)
- Message passing 관점 정리: Message Passing Neural Networks
- 한계 이해: oversmoothing, directed/edge-feature graphs, large-scale mini-batch GNN training
