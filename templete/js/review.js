// 글쓰기 버튼 이벤트 리스너
document.getElementById('writeBtn').addEventListener('click', function() {
    // 글쓰기 모달 표시
    document.getElementById('writeModal').style.display = 'block';
  });
  
  // 모달 닫기 버튼 이벤트 리스너
  document.getElementsByClassName('close')[0].addEventListener('click', function() {
    // 글쓰기 모달 숨기기
    document.getElementById('writeModal').style.display = 'none';
  });
  
  // 등록하기 버튼 이벤트 리스너
document.getElementById('submitBtn').addEventListener('click', function() {
    // 입력 값 가져오기
    var title = document.getElementById('titleInput').value.trim();
    var content = document.getElementById('contentInput').value.trim();
    // 제목과 내용이 있는 경우에만 처리
    if (title && content) {
      // 문의 목록 테이블에 행 추가
      var inquiryList = document.getElementById('inquiryList');
      var currentTime = new Date().toLocaleString();
      var indexNumber = inquiryList.rows.length; // 테이블의 현재 행 수를 인덱스 번호로 사용
      var row = inquiryList.insertRow();
      row.insertCell().textContent = indexNumber; // 인덱스 번호 셀 추가
      row.insertCell().textContent = title;
      row.insertCell().textContent = content;
      row.insertCell().textContent = currentTime;
      row.insertCell().textContent = '회원'; // 기본값으로 '회원' 설정
      
      // 입력 필드 초기화
      document.getElementById('titleInput').value = '';
      document.getElementById('contentInput').value = '';
      // 모달 닫기
      document.getElementById('writeModal').style.display = 'none';
    } else {
      alert('제목과 내용을 모두 입력해주세요.');
    }
  });
  
  
  // 모달 바깥 영역 클릭 시 모달 닫기
  window.onclick = function(event) {
    if (event.target == document.getElementById('writeModal')) {
      document.getElementById('writeModal').style.display = 'none';
    }
  };