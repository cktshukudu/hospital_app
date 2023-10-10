const stars = document.querySelectorAll(".star");
        const averageRatingElement = document.getElementById("averageRating");
        const submitBtn = document.getElementById("submitBtn");
        var rate = document.getElementById("patient");
        let rating = "{{rate}}";
        let selectedRating = 0;
        let totalRatings = 0;
        let sumRatings = 0;
  
        stars.forEach((star) => 
        {
          star.addEventListener("click", () => {
            selectedRating = parseInt(star.getAttribute("data-rating"));
            num = Number(rating);
            num -= num;
            num += selectedRating;
            rating = num;
            var doc = document.getElementById("value");
            doc.value = rating;
            console.log(rating);
            var form = document.getElementById("myForm");
            console.log(form)
            updateStars(selectedRating);
          });
        });
  
        function updateStars(selectedRating) {
          stars.forEach((star) => {
            const starRating = parseInt(star.getAttribute("data-rating"));
            if (starRating <= selectedRating) {
              star.style.color = "orange";
            } else {
              star.style.color = "#ccc";
            }
          });
        }