---
title: "Adam: A Method for Stochastic Optimization"
authors: ["Diederik P. Kingma", "Jimmy Lei Ba"]
year: 2014
source: "ICLR 2015 conference paper (arXiv:1412.6980)"
tags: [optimization, adam, adamax, sgd, adaptive-learning-rate, deep-learning, regret-bound, paper-card]
---

# 논문 전체 요약

확률적(stochastic) 목적 함수의 1차(gradient) 기반 최적화를 위한 알고리즘 **Adam**(Adaptive Moment Estimation)을 제안한다. 그래디언트의 1차 모멘트(평균)와 2차 모멘트(비중심 분산)의 지수이동평균을 추정하고, 0으로 초기화된 추정치의 편향을 해석적으로 보정한 뒤 파라미터별로 적응적 스텝을 밟는다. 구현이 단순하고 계산·메모리 비용이 적으며, 그래디언트의 대각 리스케일링에 불변이고, AdaGrad의 희소 그래디언트 처리 능력과 RMSProp의 비정상(non-stationary) 목적 함수 처리 능력을 결합했다고 주장한다. 온라인 볼록 최적화 프레임워크에서 $O(\sqrt{T})$ regret 한계를 증명하고, 로지스틱 회귀·다층 신경망·CNN·VAE 실험으로 다른 확률적 최적화 기법 대비 우위를 보인다. 무한 노름 기반 변형 **AdaMax**도 함께 제안한다. 권장 기본값은 $\alpha=0.001,\ \beta_1=0.9,\ \beta_2=0.999,\ \epsilon=10^{-8}$. (p.1)


### TL;DR

- 확률적(stochastic) 목적 함수의 1차(gradient) 기반 최적화를 위한 알고리즘 **Adam**(Adaptive Moment Estimation)을 제안한다.
- 아래 섹션의 수치, 그림, 표 장부를 원문 근거 단위로 확인한다.

### Why it matters

- 이 공개 예시 카드에서 논문의 방법, 결과, 한계, 그림·표 근거를 검토하기 위한 기본 요약 카드다.

### When to cite

- `Adam: A Method for Stochastic Optimization`의 핵심 주장, 방법, 실험 결과, 또는 한계를 근거와 함께 인용해야 할 때 사용한다.

### Do not overclaim

- 카드에 명시된 원문 근거와 `해석` 콜아웃 밖으로 주장을 확장하지 않는다.
- 정량 비교는 아래 섹션이나 `그림·표 커버리지`에 적힌 수치가 있을 때만 사용한다.

### Limitations / Failure modes / Not settled by this paper

- 이 블록은 새 한계를 추가하지 않는다. 논문이 명시한 한계와 카드의 `해석` 콜아웃, `Limitations`, `Discussion`, `한계` 섹션을 우선 근거로 사용한다.
- 명시 근거가 없는 후속 해석은 원문 확인 전까지 보류한다.

---

## 1 Introduction

**핵심 주장**
- 많은 기계학습 문제의 목적 함수는 미니배치 서브샘플링이나 드롭아웃 노이즈 때문에 본질적으로 확률적이며, 이런 경우 고차 최적화보다 1차(gradient) SGD 계열이 효율적이다.
- Adam은 1·2차 모멘트 추정으로 파라미터별 적응 학습률을 계산하며, AdaGrad(희소 그래디언트에 강함)와 RMSProp(온라인·비정상 목적에 강함)의 장점을 결합한다.
- 장점 요약: 업데이트 크기가 그래디언트 리스케일링에 불변, 스텝 크기가 하이퍼파라미터 $\alpha$로 대략 상한됨, 정상성(stationarity) 가정 불필요, 희소 그래디언트에서 작동, 자연스러운 스텝 크기 어닐링 수행. (p.1-2)

**근거·데이터 요약**
- 초록에서 명시한 설계 목표: 대규모 데이터/고차원 파라미터 문제, 노이즈·희소 그래디언트, 비정상 목적, 직관적 하이퍼파라미터. 관련 기법으로 AdaGrad, RMSProp, vSGD, AdaDelta를 든다. (p.1-2)

**원문 페이지**: p.1-2

---

## 2 Algorithm

**핵심 주장**
- Adam은 그래디언트 $g_t$의 지수이동평균 $m_t$(1차 모멘트)와 $v_t$(2차 비중심 모멘트)를 유지하고, 0 초기화로 인한 편향을 보정한 $\hat{m}_t, \hat{v}_t$로 업데이트한다.
- 유효 스텝 크기는 대략 $\alpha$로 상한되어 일종의 *trust region*을 형성하며, 업데이트는 그래디언트 스케일에 불변이다.
- $\hat{m}_t/\sqrt{\hat{v}_t}$는 신호 대 잡음비(SNR)로 해석된다 — 최적점 근처에서 SNR이 작아져 스텝이 자동으로 줄어드는 어닐링 효과가 있다.

**근거·데이터 요약**
- **알고리즘 1 (p.2)** 업데이트 규칙 (모든 연산은 원소별):
$$m_t = \beta_1 m_{t-1} + (1-\beta_1)\, g_t, \qquad v_t = \beta_2 v_{t-1} + (1-\beta_2)\, g_t^2$$
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \qquad \hat{v}_t = \frac{v_t}{1-\beta_2^t}, \qquad \theta_t = \theta_{t-1} - \alpha\, \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$
  권장 기본값 $\alpha=0.001,\ \beta_1=0.9,\ \beta_2=0.999,\ \epsilon=10^{-8}$. 효율을 위해 $\alpha_t = \alpha\cdot\sqrt{1-\beta_2^t}/(1-\beta_1^t)$로 묶어 마지막 두 줄을 $\theta_t = \theta_{t-1} - \alpha_t\, m_t/(\sqrt{v_t}+\hat{\epsilon})$ 한 줄로 대체할 수 있다.
- **유효 스텝 상한 (2.1, p.2-3)**: $\Delta_t = \alpha\,\hat{m}_t/\sqrt{\hat{v}_t}$에 대해 $(1-\beta_1) > \sqrt{1-\beta_2}$이면 $|\Delta_t| \le \alpha\,(1-\beta_1)/\sqrt{1-\beta_2}$, 그 외에는 $|\Delta_t| \le \alpha$. 보통의 경우 $|\hat{m}_t/\sqrt{\hat{v}_t}| \approx \pm 1$이어서 $|\Delta_t| \lessapprox \alpha$.
- **스케일 불변 (p.3)**: 그래디언트를 $c$배 해도 $c\,\hat{m}_t / \sqrt{c^2\,\hat{v}_t} = \hat{m}_t/\sqrt{\hat{v}_t}$로 상쇄.

> [!note] 해석
> $\epsilon$이 $\sqrt{\hat{v}_t}$ *바깥*에 더해지는 위치는 이후 구현들(TensorFlow/PyTorch의 eps 위치, "epsilon-hat" 변형)에서 미묘한 차이를 낳는 지점으로, 재현 시 프레임워크별 기본값·위치를 확인할 필요가 있다.

**원문 페이지**: p.2-3

---

## 3 Initialization Bias Correction

**핵심 주장**
- $m_0 = v_0 = 0$ 초기화 때문에 모멘트 추정치는 학습 초기와 감쇠율이 1에 가까울 때($\beta$가 1에 근접) 0 쪽으로 편향된다.
- 이 편향은 $(1-\beta^t)$로 나누는 보정으로 정확히 상쇄할 수 있다.

**근거·데이터 요약**
- 2차 모멘트 전개: $v_t = (1-\beta_2)\sum_{i=1}^{t} \beta_2^{t-i}\, g_i^2$ 로부터
$$\mathbb{E}[v_t] = \mathbb{E}[g_t^2]\cdot(1-\beta_2^t) + \zeta$$
  ($\zeta$는 $\mathbb{E}[g_i^2]$가 정상적(stationary)이면 0, 아니면 과거에 작은 가중치를 주도록 $\beta_1$을 잡아 작게 유지 가능). 따라서 $(1-\beta_2^t)$로 나누면 편향이 제거된다. 1차 모멘트도 동일한 유도. (p.3)
- 희소 그래디언트 상황에서는 2차 모멘트를 신뢰성 있게 추정하려면 작은 $1-\beta_2$ (즉 $\beta_2\to1$)로 많은 그래디언트를 평균해야 하는데, 보정이 없으면 이 경우 초기 스텝이 훨씬 커진다. (p.3)

**원문 페이지**: p.3

---

## 4 Convergence Analysis

**핵심 주장**
- 온라인 볼록 최적화 프레임워크(Zinkevich, 2003)에서 Adam의 regret $R(T) = \sum_{t=1}^{T}[f_t(\theta_t) - f_t(\theta^*)]$가 $O(\sqrt{T})$임을 증명한다 (정리 4.1, 따름정리 4.2).
- 데이터 특징이 희소하고 그래디언트가 자주 0일 때, 한계의 적응항들이 상한 $dG_\infty\sqrt{T}$보다 훨씬 작아질 수 있어 AdaGrad처럼 $O(\log d\,\sqrt{T})$ 수준의 개선을 기대할 수 있다.
- $\beta_1$을 $\beta_{1,t} = \beta_1\lambda^{t-1}$로 감쇠시키는 것이 이론적으로 중요하며, 수렴에 $\alpha_t = \alpha/\sqrt{t}$ 감쇠를 사용한다.

**근거·데이터 요약**
- **정리 4.1 (p.4)** 가정: 그래디언트 유계 $\|\nabla f_t(\theta)\|_2 \le G$, $\|\nabla f_t(\theta)\|_\infty \le G_\infty$; 파라미터 간 거리 유계 $\|\theta_n - \theta_m\|_2 \le D$, $\|\theta_n - \theta_m\|_\infty \le D_\infty$; $\beta_1, \beta_2 \in [0,1)$이고 $\frac{\beta_1^2}{\sqrt{\beta_2}} < 1$; $\lambda \in (0,1)$. 이때
$$R(T) \le \frac{D^2}{2\alpha(1-\beta_1)}\sum_{i=1}^{d}\sqrt{T\hat{v}_{T,i}} \;+\; \frac{\alpha(1+\beta_1)G_\infty}{(1-\beta_1)\sqrt{1-\beta_2}\,(1-\gamma)^2}\sum_{i=1}^{d}\|g_{1:T,i}\|_2 \;+\; \sum_{i=1}^{d}\frac{D_\infty^2 G_\infty\sqrt{1-\beta_2}}{2\alpha\beta_1(1-\lambda)^2}$$
  (여기서 $\gamma \triangleq \frac{\beta_1^2}{\sqrt{\beta_2}}$). 적응항 $\sum_i \sqrt{T\hat{v}_{T,i}} \le dG_\infty\sqrt{T}$, $\sum_i \|g_{1:T,i}\|_2 \le dG_\infty\sqrt{T}$ 이지만 희소 그래디언트에서는 훨씬 작다.
- **따름정리 4.2 (p.4)**: 같은 가정 아래 $\frac{R(T)}{T} = O\!\left(\frac{1}{\sqrt{T}}\right)$, 즉 $\lim_{T\to\infty} R(T)/T = 0$ — 평균 regret 수렴.
- 보통 사용하는 $\beta_2$가 1에 가까운 설정에서 $\hat{v}$의 감쇠가 느린데, $\beta_{1,t}$ 감쇠(예: $\lambda = 1-10^{-8}$)는 실무에서 거의 영향이 없다고 언급. (p.4-5)

> [!note] 해석
> 이 수렴 증명은 이후 Reddi et al. (ICLR 2018, "On the Convergence of Adam and Beyond")에서 오류가 지적되어, 단순 볼록 반례에서 Adam이 수렴하지 않음이 보여졌고 AMSGrad가 수정안으로 제시됐다. 따라서 이 절의 정리는 역사적 의의로 읽되 그대로 신뢰해서는 안 된다. 실전에서의 Adam 유효성 자체는 별개 문제로 광범위하게 재확인되었다.

**원문 페이지**: p.4-5 (증명 전체는 부록 10.1, p.12-15)

---

## 5 Related Work

**핵심 주장**
- 가장 직접 관련된 기법은 RMSProp(+모멘텀)과 AdaGrad이며, Adam은 두 방법의 핵심 약점을 보완한다.
- RMSProp+모멘텀은 리스케일된 그래디언트에 모멘텀을 적용하지만 Adam은 1·2차 모멘트의 이동평균 자체로 업데이트하며, RMSProp에는 편향 보정이 없어 $\beta_2$가 1에 가까울 때 매우 큰 스텝 크기와 발산까지 일으킬 수 있다(6.4절에서 실증).
- AdaGrad($\theta_{t+1} = \theta_t - \alpha\, g_t / \sqrt{\sum_{i=1}^t g_i^2}$)는 Adam에서 $\beta_1 = 0$, $\beta_2 \to 1$ (무한소 근접), $\alpha_t = \alpha\, t^{-1/2}$ 어닐링을 취한 특수 극한에 대응한다 — 단, 편향 보정이 없으면 이 대응이 성립하지 않는다.

**근거·데이터 요약**
- 그 밖에 vSGD(헤시안 대각 추정 기반 자동 스텝), AdaDelta, natural Newton method, SFO(미니배치 기반 준뉴턴), 자연 그래디언트(Fisher 정보 행렬 전제조건자) 등을 인접 연구로 정리. Adam의 $\hat{v}$ 전제조건자는 Fisher 정보 행렬 대각 근사보다 보수적인($\sqrt{\cdot}$를 취한) 적응으로 위치 지움. (p.5)

**원문 페이지**: p.5

---

## 6 Experiments

**핵심 주장**
- 로지스틱 회귀(밀집·희소 특징), 다층 신경망, CNN, VAE에 걸쳐 Adam이 비교 대상(SGD+Nesterov, AdaGrad, RMSProp, AdaDelta, SFO) 대비 동등하거나 더 빠르게 수렴한다.
- 희소 특징에서는 AdaGrad의 장점을 그대로 흡수하고, 노이즈 많은 비볼록 문제에서도 안정적이다.
- 모든 실험에서 하이퍼파라미터는 동일 초기화 후 학습률만 밀집 탐색해 최적값으로 비교했다.

**근거·데이터 요약**
- **6.1 로지스틱 회귀 + 그림 1 (p.5-6)**: L2 정규화 다중클래스 로지스틱 회귀, $\alpha_t = \alpha/\sqrt{t}$ 감쇠, 미니배치 128.
  - **그림 1 좌 (MNIST Logistic Regression)**: x축 전체 데이터셋 반복(에포크) 0~45, y축 training cost 약 0.2~0.7. 3곡선(AdaGrad, SGDNesterov, Adam). Adam과 SGD+Nesterov는 초반 5~10 에포크에 가파르게 떨어져 0.25 부근으로 수렴하며 서로 유사; AdaGrad는 전 구간에서 그 위에 머물며 훨씬 느리게 감소.
  - **그림 1 우 (IMDB BoW Logistic Regression)**: 10,000차원 희소 bag-of-words 특징, BoW에 50% 드롭아웃 노이즈 적용. x축 0~160 에포크, y축 training cost 0.20~0.50. 4곡선(Adagrad+dropout, RMSProp+dropout, SGDNesterov+dropout, Adam+dropout)이 드롭아웃 때문에 요동. 희소 특징에서는 AdaGrad가 SGD+Nesterov를 큰 폭으로 능가하는데, Adam은 AdaGrad만큼 빠르게 약 0.25 수준의 최저 비용에 도달; SGDNesterov·RMSProp은 0.30 이상에 머묾.
- **6.2 다층 신경망 + 그림 2 (p.6-7)**: MNIST, 은닉층 2개 × 1000 유닛, ReLU, 미니배치 128, 교차엔트로피 + L2 weight decay.
  - **그림 2(a)**: 드롭아웃 확률 적용 모델. x축 0~200 에포크, y축 training cost(로그 스케일, $10^{-2}$~$10^0$). 5곡선(AdaGrad, RMSProp, SGDNesterov, AdaDelta, Adam) 중 Adam이 전 구간 가장 아래에서 가장 빠르게 감소.
  - **그림 2(b)**: 확률적 정규화 없는 결정론적 비용 함수에서 준뉴턴 계열 SFO(Sohl-Dickstein et al., 2014)와 비교(2개 서브플롯). Adam이 반복 수 기준으로도 SFO보다 빠르고, SFO는 반복당 계산이 5~10배 느린 데다 곡률 추정 메모리가 미니배치 수에 선형이라 실시간(wall-clock) 격차는 더 큼.
- **6.3 CNN + 그림 3 (p.6-7)**: CIFAR-10, c64-c64-c128-1000 구조 — 5×5 합성곱 64채널과 stride 2의 3×3 맥스풀링이 교차하는 3단 + ReLU 1000유닛 완전연결층. 입력 화이트닝, 입력층·완전연결층에 드롭아웃 노이즈, 미니배치 128.
  - **그림 3 좌 (첫 3 에포크)**: x축 0.5~3.0 에포크, y축 training cost(선형). 6곡선(AdaGrad, AdaGrad+dropout, SGDNesterov, SGDNesterov+dropout, Adam, Adam+dropout). 초반에는 Adam과 AdaGrad 모두 빠르게 비용을 낮춤.
  - **그림 3 우 (45 에포크)**: y축 로그 스케일($10^{-4}$~$10^2$ 부근). 장기적으로는 Adam과 SGD가 AdaGrad보다 훨씬 빠르게 수렴하고 AdaGrad는 높은 비용에서 정체. Adam은 SGD+Nesterov 대비로는 근소한 개선이지만, SGD처럼 층별 학습률을 수동 튜닝할 필요 없이 자동 적응한다는 점을 강조.
  - 저자 분석: CNN에서는 $\hat{v}_t$가 몇 에포크 만에 0으로 소멸해 $\epsilon$에 지배되므로 2차 모멘트가 비용 지형 근사로는 부실하며, 속도 향상은 주로 1차 모멘트를 통한 미니배치 분산 저감에서 온다. (p.7)
- **6.4 편향 보정 항 검증 + 그림 4 (p.8)**: VAE(은닉 500 softplus 유닛, 50차원 구형 가우시안 잠재변수) 학습에서 $\beta_1 \in \{0, 0.9\}$, $\beta_2 \in \{0.99, 0.999, 0.9999\}$, $\log_{10}(\alpha) \in \{-5,\dots,-1\}$ 전 조합을 비교.
  - **그림 4**: (a) 10 에포크 후, (b) 100 에포크 후 두 패널, 각각 $\beta_1$(행 2) × $\beta_2$(열 3)의 6개 서브플롯. x축 $\log_{10}(\alpha)$, y축 손실. 빨간 선 = 편향 보정 있음(Adam), 초록 선 = 보정 없음(RMSProp에 대응). $\beta_2$가 1에 가까울수록(특히 0.9999) 보정 없는 초록 선이 학습 초기에 불안정·발산 스파이크를 보이는 반면, 빨간 선은 전 영역에서 안정. 최고 성능은 작은 $1-\beta_2$ + 편향 보정 조합이며, 학습 후반(은닉 유닛이 특화되어 그래디언트가 희소해질 때) 차이가 더 뚜렷. 결론: **Adam은 하이퍼파라미터 설정과 무관하게 RMSProp과 같거나 더 좋았다**.

**원문 페이지**: p.5-8

---

## 7 Extensions

**핵심 주장**
- **AdaMax (7.1)**: 2차 모멘트의 $L^2$ 노름을 $L^p$로 일반화한 뒤 $p\to\infty$ 극한을 취하면, 놀랍도록 단순하고 수치적으로 안정한 알고리즘이 나온다.
- AdaMax의 무한 노름 추정 $u_t$는 max 연산 기반이라 0 초기화 편향 보정이 필요 없고, 업데이트 크기는 $|\Delta_t| \le \alpha$로 더 깔끔하게 상한된다.
- **시간 평균화 (7.2)**: 마지막 반복값은 노이즈가 크므로 Polyak–Ruppert 평균화의 지수 감쇠 버전으로 일반화 성능을 높일 수 있다.

**근거·데이터 요약**
- **알고리즘 2 — AdaMax (p.9)**:
$$u_t = \max(\beta_2 \cdot u_{t-1},\ |g_t|), \qquad \theta_t = \theta_{t-1} - \frac{\alpha}{1-\beta_1^t}\cdot\frac{m_t}{u_t}$$
  $u_t = \lim_{p\to\infty}(v_t^{(p)})^{1/p} = \max\big(\beta_2^{t-1}|g_1|,\ \beta_2^{t-2}|g_2|,\ \dots,\ |g_t|\big)$ 의 재귀형. 권장값 $\alpha=0.002,\ \beta_1=0.9,\ \beta_2=0.999$. ($\alpha/(1-\beta_1^t)$가 편향 보정된 학습률.)
- **시간 평균화 (p.9)**: $\bar{\theta}_t = \beta_2\cdot\bar{\theta}_{t-1} + (1-\beta_2)\,\theta_t$, 편향 보정 $\hat{\theta}_t = \bar{\theta}_t/(1-\beta_2^t)$. 알고리즘 1·2의 내부 루프에 한 줄 추가로 구현 가능.

**원문 페이지**: p.8-9

---

## 8 Conclusion

**핵심 주장**
- 확률적 목적 함수의 그래디언트 기반 최적화를 위한 단순·효율적 알고리즘을 제안했고, 대규모 데이터셋/고차원 파라미터 공간을 겨냥했다.
- AdaGrad의 희소 그래디언트 대응력과 RMSProp의 비정상 목적 대응력을 결합했으며, 구현이 쉽고 메모리 요구가 적다.
- 실험이 볼록 문제 수렴률 분석과 부합했으며, Adam은 기계학습 분야의 광범위한 비볼록 최적화 문제에 강건하고 잘 맞는다고 결론짓는다.

**근거·데이터 요약**
- 9절(Acknowledgments)과 참고문헌이 p.10-11에 이어진다. (p.9-11)

> [!note] 해석
> 이 논문은 이후 딥러닝 학습의 사실상 표준 옵티마이저가 되었고(인용 수 기준 역대 최상위권), AdamW(weight decay 분리, 2017), AMSGrad(수렴 수정, 2018) 등 파생 계보의 기점이다. 본문이 주장하는 "하이퍼파라미터 튜닝이 거의 불필요"는 실무에서 대체로 성립하지만, 학습률 $\alpha$와 warmup은 여전히 과제별 튜닝 대상이라는 것이 이후의 경험적 합의다.

**원문 페이지**: p.9-10

---

## Appendix 하이라이트 (10 Convergence Proof)

**핵심 주장**
- 정리 4.1의 완전한 증명을 제공한다. 볼록 함수의 접평면 하한(보조정리 10.2)으로 regret을 상계하고, Adam 업데이트 규칙을 대입해 항별로 묶는 구조다.

**근거·데이터 요약**
- **보조정리 10.3 (p.12)**: 유계 그래디언트 가정 하에 $\sum_{t=1}^{T}\sqrt{g_{t,i}^2/t} \le 2G_\infty\|g_{1:T,i}\|_2$ — $T$에 대한 귀납법으로 증명.
- **보조정리 10.4 (p.13)**: $\gamma \triangleq \frac{\beta_1^2}{\sqrt{\beta_2}} < 1$일 때 $\sum_{t=1}^{T} \frac{\hat{m}_{t,i}^2}{\sqrt{t\,\hat{v}_{t,i}}} \le \frac{2}{1-\gamma}\frac{1}{\sqrt{1-\beta_2}}\|g_{1:T,i}\|_2$ — 산술–기하급수 상한 활용.
- **정리 10.5 (p.13-15)**: 위 보조정리들과 $\|\theta_t-\theta^*\|_2 \le D$, $\|\theta_m-\theta_n\|_\infty \le D_\infty$ 가정을 결합해 본문 정리 4.1의 3항 regret 한계를 도출. $\beta_{1,t} = \beta_1\lambda^{t-1}$ 감쇠가 마지막 항의 $(1-\lambda)^2$ 분모를 만든다.

> [!note] 해석
> Reddi et al. (2018)이 지적한 결함은 이 부록의 전개 중 $\Gamma_t$에 해당하는 양(스텝 크기 역수의 단조성)이 양수라는 암묵적 가정에 있다 — Adam에서는 이 양이 음수가 될 수 있어 증명이 깨진다. 부록을 읽을 때 이 지점을 염두에 둘 것.

**원문 페이지**: p.12-15

---

## 그림·표 커버리지

- 원문(텍스트 휴리스틱 추출): Figure 1-4 / Table 없음
- 카드에서 언급 확인: Figure 1-4 / Table 없음
- 미확인 항목 없음
- (기계 백필 장부 — 휴리스틱 기반이므로 심층 감사 시 갱신)
