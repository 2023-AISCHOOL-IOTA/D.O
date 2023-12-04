
Vue.createApp({
  data() {
    return {
      count: 0,
      items: [],
      itemStyles: [],
      lineStyles: [],
      current: 0,
      userInput: "",
      numberOfItems: [], // 사용자가 설정할 항목 수
    };
  },
  computed: {
    segment() {
      return 360 / this.items.length;
    },
    offset() {
      return this.segment / 2;
    },
    angle() {
      if (this.count === 0) {
        return 0;
      }
      let temp = -this.current * this.segment;
      let randomOffset = Math.floor(Math.random() * this.segment);
      let cycle = this.count * 360 * 5;
      return temp + randomOffset + cycle; // 오른쪽으로 회전하도록 부호 변경
    },
    rouletteStyle() {
      return {
        transform: "rotate(" + this.angle + "deg)",
      };
    },
    currentItem() {
      return this.items[this.current];
    },
  },
  methods: {
    initializeItems() {
      this.items = Array.from({ length: this.numberOfItems }, () => ({
        value: "",
      }));
      this.recalculateStyles();
    },
    recalculateStyles() {
      this.itemStyles = [];
      this.lineStyles = [];
      this.items.forEach((el, idx) => {
        const segment = 360 / this.items.length;
        const offset = segment / 2;
        this.itemStyles.push({
          transform: "rotate(" + segment * idx + "deg)",
        });
        this.lineStyles.push({
          transform: "rotate(" + (segment * idx + offset) + "deg)",
        });
      });
    },
    play() {
      this.count++;
      this.current = Math.floor(Math.random() * this.items.length);
    },
    updateItem() {
      if (this.userInput.trim() !== "") {
        const emptyIndex = this.items.findIndex((item) => item.value === "");
        if (emptyIndex !== -1) {
          this.items[emptyIndex].value = this.userInput;
          this.userInput = ""; // 입력 필드 초기화
        }
      }
    },
  },
}).mount("#app");

// 메시지 보내기 이벤트 리스너들
document.getElementById("push-btn").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    updateItem();
  }
});
