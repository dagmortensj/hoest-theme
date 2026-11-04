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
    explicit Vektor(T x = T{}) noexcept : data_{x} { antall_ <<= 1; }
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
    for (auto& [navn, masse] : liste) { masse *= 1.5; std::cout << navn << '\n'; }
    try { throw std::runtime_error("feil"); } catch (const std::exception& e) {}
    return tung(*jord) ? 0 : 1;
}

// Vanskelige tilfeller: operatoroverlasting, maler, lambdaer, strenger og bitoperasjoner
namespace fysikk {
template <Tall T, std::size_t N>
constexpr Vektor<T, N> operator+(const Vektor<T, N>& a, const Vektor<T, N>&) noexcept { return a; }
template <typename T> concept Legemeaktig = requires(T t) { { t.masse } -> std::convertible_to<double>; };
struct Punkt {
    double x{}, y{};
    auto operator<=>(const Punkt&) const = default;
    Punkt& operator+=(const Punkt& p) { x += p.x; y += p.y; return *this; }
    Punkt operator-() const { return {-x, -y}; }
};
template <auto V> inline constexpr auto verdi = V;
}  // namespace fysikk
int vanskelig(int argc, char** argv) {
    using namespace std::string_literals; using fysikk::Punkt;
    auto s = "a + b == c"s + R"(rå \n streng)" + "\t\"" + '\n'; auto tall = 0b1010 | 0x0F & ~0 ^ 1 << 2; tall >>= 1;
    Punkt p{1.0, 2.0}, q = -p; p += q; bool lik = p == q && (p <=> q) == 0 && !(p != q);
    auto f = [tall, &p](auto x) mutable -> decltype(x) { tall++; p.x *= x; return x * 2 + tall; };
    int* ptr = &argc; int& ref = *ptr; ref = ref++ + --ref; std::cout << f(1.5) << " " << (ptr ? *ptr : -1) << '\n';
    std::vector<int> v(3, 0); for (auto& e : v) e = e % 2 == 0 ? e / 2 : e * 3 + 1;
    try { throw std::out_of_range{"feil"}; } catch (...) { return static_cast<int>(sizeof v); }
    goto slutt; slutt: return fysikk::verdi<42> + lik + (argv != nullptr);
}
