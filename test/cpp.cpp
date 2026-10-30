// C++: navnerom, maler, klasser, lambdaer og standardbiblioteket
#include <iostream>
#include <memory>
#include <string>
#include <vector>

namespace fysikk {
template <typename T>
concept Tall = std::is_arithmetic_v<T>;
constexpr double G = 6.674e-11;

template <Tall T, std::size_t N = 3>
class Vektor final {
public:
    explicit Vektor(T x = T{}) noexcept : data_{x} {}
    [[nodiscard]] T& operator[](std::size_t i) { return data_[i]; }
    virtual ~Vektor() = default;
private:
    T data_[N];
    static inline int antall_ = 0;
};

struct Legeme { std::string navn; double masse{1.0}; };
enum class Farge : int { Rod, Gronn };

}  // namespace fysikk

int main() {
    using fysikk::Legeme;
    auto jord = std::make_unique<Legeme>(Legeme{"Jorda", 5.972e24});
    std::vector<Legeme> liste{*jord, {"Mars", 6.4e23}};
    auto tung = [&liste](const Legeme& l) -> bool { return l.masse > 1e24; };
    for (const auto& [navn, masse] : liste) std::cout << navn << '\n';
    try { throw std::runtime_error("feil"); } catch (const std::exception& e) {}
    return tung(*jord) ? 0 : 1;
}
